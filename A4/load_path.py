"""Geometric screening of potential load paths; no structural capacity assessment.

All geometry and tolerances are in metres. Functions may be imported by a manager.
"""
from collections import Counter, deque
from dataclasses import dataclass, field
import csv
import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element as ifc_element
import ifcopenshell.util.unit as ifc_unit
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

STR_TYPES = ('IfcColumn', 'IfcBeam', 'IfcSlab', 'IfcWall')
GEO_TYPES = ('IfcColumn', 'IfcWall', 'IfcFooting', 'IfcPile')
EPS = 1e-6


@dataclass
class Element:
    key: str
    source: str
    guid: str
    ifc_class: str
    name: str
    storey: str
    materials: list
    profiles: list
    minimum: list | None = None
    maximum: list | None = None
    bottom: object = None
    top: object = None
    error: str = ''
    terminal: bool = False
    terminal_basis: str = ''
    issues: list = field(default_factory=list)
    entity: object = field(default=None, repr=False)
    shape: object = field(default=None, repr=False)
    review_connections: list = field(default_factory=list)
    prism_footprint: object = field(default=None, repr=False)


def _surface(vertices, faces, z):
    """Union of horizontal triangles at an extreme; holes remain holes."""
    polygons = []
    for triangle in vertices[faces]:
        if np.max(np.abs(triangle[:, 2] - z)) <= EPS:
            p = Polygon(triangle[:, :2])
            if p.area > EPS ** 2:
                polygons.append(p)
    return unary_union(polygons)


def _vertical_prism(vertices, faces, bottom, top):
    """Prove a closed, straight vertical prism before using a footprint fallback.

    The mesh must have two Z planes, matching end faces, vertical side faces,
    and exactly two incident triangles per mesh edge. This is not an AABB test.
    """
    if bottom.is_empty or top.is_empty or bottom.symmetric_difference(top).area > EPS ** 2:
        return None
    zmin, zmax = vertices[:, 2].min(), vertices[:, 2].max()
    if zmax - zmin <= EPS:
        return None
    if not np.all((np.abs(vertices[:, 2] - zmin) <= EPS) |
                  (np.abs(vertices[:, 2] - zmax) <= EPS)):
        return None
    triangles = vertices[faces]
    for triangle in triangles:
        if np.ptp(triangle[:, 2]) <= EPS:
            continue
        normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
        if abs(normal[2]) > EPS * max(np.linalg.norm(normal), EPS):
            return None
    mesh_edges = np.sort(np.vstack([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1)
    _, incidence = np.unique(mesh_edges, axis=0, return_counts=True)
    return bottom if np.all(incidence == 2) else None


def CAPT_elements(model, source):
    """Extract metadata, world-space SI geometry and horizontal bearing faces."""
    settings = ifcopenshell.geom.settings()
    settings.set('use-world-coords', True)
    result = []
    unit_scale = ifc_unit.calculate_unit_scale(model)
    for kind in STR_TYPES if source == 'STR' else GEO_TYPES:
        for obj in model.by_type(kind):
            container = ifc_element.get_container(obj)
            materials = sorted({m.Name for m in ifc_element.get_materials(obj) if m.Name})
            profiles = []
            if obj.Representation:
                for entity in model.traverse(obj.Representation):
                    if entity.is_a('IfcProfileDef'):
                        # Attribute names retain their IFC spelling. Dimensions are SI.
                        data = {'type': entity.is_a(), 'name': entity.ProfileName}
                        for attr in ('XDim', 'YDim', 'Radius', 'OverallWidth',
                                     'OverallDepth', 'WallThickness', 'WebThickness',
                                     'FlangeThickness'):
                            value = getattr(entity, attr, None)
                            if value is not None:
                                data[attr + '_m'] = value * unit_scale
                        if data not in profiles:
                            profiles.append(data)
            row = Element(f'{source}:{obj.GlobalId}', source, obj.GlobalId, obj.is_a(),
                          obj.Name or '', container.Name if container else '', materials, profiles)
            if not row.storey:
                row.issues.append('missing_storey')
            if not materials:
                row.issues.append('missing_material')
            if kind in ('IfcBeam', 'IfcColumn') and not profiles:
                row.issues.append('missing_explicit_profile')
            try:
                shape = ifcopenshell.geom.create_shape(settings, obj)
                vertices = np.array(shape.geometry.verts).reshape(-1, 3)
                faces = np.array(shape.geometry.faces).reshape(-1, 3)
                if not len(vertices) or not len(faces) or not np.isfinite(vertices).all():
                    raise ValueError('Empty or non-finite mesh')
                if faces.min() < 0 or faces.max() >= len(vertices):
                    raise ValueError('Mesh face references an invalid vertex')
                row.minimum = vertices.min(axis=0).tolist()
                row.maximum = vertices.max(axis=0).tolist()
                row.bottom = _surface(vertices, faces, row.minimum[2])
                row.top = _surface(vertices, faces, row.maximum[2])
                # Keep the owning shape alive for IfcOpenShell's intersection tree.
                row.entity = obj
                row.shape = shape
                row.prism_footprint = _vertical_prism(vertices, faces, row.bottom, row.top)
                if row.bottom.is_empty:
                    row.issues.append('no_horizontal_bottom_at_global_minimum')
                if row.top.is_empty:
                    row.issues.append('no_horizontal_top_at_global_maximum')
                if min(np.subtract(row.maximum, row.minimum)) <= EPS:
                    row.issues.append('degenerate_geometry')
            except (RuntimeError, ValueError, TypeError) as ex:
                row.error = str(ex)
                row.issues.append('geometry_unavailable')
            result.append(row)
    return result


def mark_terminals(elements, foundation_ids):
    """Only explicitly listed GEO elements are terminals; no class-only inference."""
    found = {e.guid for e in elements if e.source == 'GEO'}
    missing = set(foundation_ids) - found
    if missing:
        raise ValueError(f'Foundation IDs absent from GEO: {sorted(missing)}')
    for e in elements:
        e.terminal = False
        e.terminal_basis = ''
        if e.source == 'GEO' and e.guid in foundation_ids:
            if 'temporary' in e.name.lower():
                raise ValueError(f'Temporary element cannot be a terminal: {e.guid}')
            e.terminal = True
            e.terminal_basis = 'Project-specific provisional foundation list; review required'


def CONN_supports(elements, tolerance_m=0.02):
    """Find potential horizontal bearing contacts, first AABB then face polygons.

    Returned edges retain the original base-to-top rule. Actual STR beam/slab
    intersections with lower STR columns/walls are recorded separately on each
    Element, never silently accepted as bearing edges.
    """
    if tolerance_m < 0 or not np.isfinite(tolerance_m):
        raise ValueError('Tolerance must be a finite non-negative number')
    edges = []
    valid = [e for e in elements if e.minimum is not None and not e.error]
    for upper in valid:
        if upper.source != 'STR' or upper.bottom is None or upper.bottom.is_empty:
            continue
        for lower in valid:
            if upper.key == lower.key or lower.top is None or lower.top.is_empty:
                continue
            # Unlisted GEO objects cannot silently become foundation supports.
            if lower.source == 'GEO' and not lower.terminal:
                continue
            if lower.minimum[2] + lower.maximum[2] >= upper.minimum[2] + upper.maximum[2] - EPS:
                continue
            gap = upper.minimum[2] - lower.maximum[2]
            if abs(gap) > tolerance_m + EPS:
                continue
            if any(upper.maximum[i] < lower.minimum[i] - tolerance_m - EPS or
                   lower.maximum[i] < upper.minimum[i] - tolerance_m - EPS for i in (0, 1)):
                continue
            area = upper.bottom.intersection(lower.top).area
            reference_area = min(upper.bottom.area, lower.top.area)
            overlap_ratio = area / reference_area if reference_area > 0 else 0.0
            lateral_gap = upper.bottom.distance(lower.top)
            if area <= EPS ** 2 and lateral_gap > tolerance_m + EPS:
                continue
            # At zero tolerance, a line/point touch is not a bearing area.
            if area <= EPS ** 2 and tolerance_m == 0:
                continue
            edges.append({'upper': upper.key, 'lower': lower.key,
                          'vertical_gap_m': round(gap, 8),
                          'horizontal_gap_m': round(lateral_gap, 8),
                          'overlap_area_m2': round(area, 8),
                          'overlap_ratio_of_smaller_face': round(overlap_ratio, 8),
                          'contact': 'AREA_CONTACT' if area > EPS ** 2 and abs(gap) <= EPS
                          else 'WITHIN_TOLERANCE_REVIEW'})
    _review_intersections(elements, edges, tolerance_m)
    return edges


def _review_intersections(elements, bearing_edges, tolerance_m):
    """Identify mesh intersections, without inferring structural connection capacity.

    Only a beam/slab and a lower column/wall in STR are considered. The lower
    element must start below the upper element and end no higher than its top.
    This excludes walls/columns that simply continue through a storey. The
    reported bounding-box vertical overlap is not a penetration measurement.
    """
    for e in elements:
        e.review_connections.clear()
    valid = [e for e in elements if e.source == 'STR' and e.shape is not None
             and e.entity is not None and not e.error]
    uppers = [e for e in valid if e.ifc_class in ('IfcBeam', 'IfcSlab')]
    lowers = [e for e in valid if e.ifc_class in ('IfcColumn', 'IfcWall', 'IfcWallStandardCase')]
    if not uppers or not lowers:
        return
    tree = ifcopenshell.geom.tree(backend='opencascade.trianglebvh')
    for e in valid:
        tree.add_element(e.shape)
    upper_by_guid = {e.guid: e for e in uppers}
    lower_by_guid = {e.guid: e for e in lowers}
    bearing_pairs = {(x['upper'], x['lower']) for x in bearing_edges}
    clashes = tree.clash_intersection_many(
        [e.entity for e in uppers], [e.entity for e in lowers],
        tolerance=EPS, check_all=True)
    pairs = {}
    for clash in clashes:
        a, b = clash.a.get_argument(0), clash.b.get_argument(0)
        upper, lower = upper_by_guid.get(a), lower_by_guid.get(b)
        if upper is None or lower is None:
            upper, lower = upper_by_guid.get(b), lower_by_guid.get(a)
        if upper is None or lower is None:
            continue
        pairs[(upper.key, lower.key)] = (upper, lower, 'IFCOPENSHELL_MESH_INTERSECTION')
    # Mesh clash detection may miss exactly aligned/coplanar prism boundaries.
    # Use an independent exact prism-overlap test only for proven closed prisms.
    for upper in uppers:
        if upper.prism_footprint is None:
            continue
        for lower in lowers:
            if lower.prism_footprint is None:
                continue
            if min(upper.maximum[2], lower.maximum[2]) <= max(upper.minimum[2], lower.minimum[2]) + EPS:
                continue
            if upper.prism_footprint.intersection(lower.prism_footprint).area > EPS ** 2:
                pairs.setdefault((upper.key, lower.key), (upper, lower, 'CLOSED_VERTICAL_PRISM_OVERLAP'))
    for pair in sorted(pairs):
        upper, lower, evidence = pairs[pair]
        if pair in bearing_pairs:
            continue
        if lower.minimum[2] >= upper.minimum[2] - EPS:
            continue
        if lower.maximum[2] > upper.maximum[2] + tolerance_m + EPS:
            continue
        if lower.minimum[2] + lower.maximum[2] >= upper.minimum[2] + upper.maximum[2] - EPS:
            continue
        gap = upper.minimum[2] - lower.maximum[2]
        if gap >= -EPS:
            continue
        overlap = min(upper.maximum[2], lower.maximum[2]) - max(upper.minimum[2], lower.minimum[2])
        upper.review_connections.append({
            'upper': upper.key, 'lower': lower.key,
            'contact': 'GEOMETRIC_INTERSECTION_REVIEW',
            'vertical_gap_m': round(gap, 8),
            'bbox_vertical_overlap_m': round(overlap, 8),
            'intersection_evidence': evidence,
            'used_in_bearing_graph': False,
            'reason': 'Intersecting solids may indicate a joint or a modelling clash; review required'})


def _paths_to_terminals(reverse, terminals):
    """Map each reachable element to its next step on a shortest path."""
    next_step = dict.fromkeys(terminals)
    queue = deque(terminals)
    while queue:
        lower = queue.popleft()
        for upper in reverse[lower]:
            if upper not in next_step:
                next_step[upper] = lower
                queue.append(upper)
    return next_step


def _example_path(key, next_step):
    if key not in next_step:
        return []
    path = []
    while key is not None:
        path.append(key)
        key = next_step[key]
    return path


def CHEK_paths(elements, edges):
    """Reverse BFS finds an example path, with explicit unresolved branch reporting."""
    by_key = {e.key: e for e in elements}
    supports = {k: [] for k in by_key}
    reverse = {k: [] for k in by_key}
    for edge in edges:
        supports[edge['upper']].append(edge['lower'])
        reverse[edge['lower']].append(edge['upper'])
    terminals = [e.key for e in elements if e.terminal and e.minimum is not None and not e.error]
    next_step = _paths_to_terminals(reverse, terminals)
    # The intersection scenario has its own graph and its own example paths.
    review_edges = [edge for e in elements for edge in e.review_connections]
    review_reverse = {k: list(v) for k, v in reverse.items()}
    for edge in review_edges:
        review_reverse[edge['lower']].append(edge['upper'])
    review_next = _paths_to_terminals(review_reverse, terminals)
    review_pairs = {(x['upper'], x['lower']) for x in review_edges}
    rows = []
    for e in elements:
        if e.source != 'STR':
            continue
        path = _example_path(e.key, next_step)
        review_path = [] if path else _example_path(e.key, review_next)
        review_links = [{'upper': a, 'lower': b, 'contact': 'GEOMETRIC_INTERSECTION_REVIEW'}
                        for a, b in zip(review_path, review_path[1:]) if (a, b) in review_pairs]
        unresolved = set()
        visited = set()
        stack = [e.key]
        while stack:
            k = stack.pop()
            if k in visited:
                continue
            visited.add(k)
            if not supports[k] and not by_key[k].terminal:
                unresolved.add(k)
            stack.extend(supports[k])
        if e.error or e.bottom is None or e.bottom.is_empty:
            status = 'INSUFFICIENT_GEOMETRY'
        elif path:
            status = ('POTENTIAL_PATH_FOUND_WITH_UNRESOLVED_BRANCHES' if unresolved
                      else 'POTENTIAL_PATH_FOUND')
        elif review_path:
            status = 'REVIEW_PATH_VIA_INTERSECTION'
        else:
            status = 'NO_PATH_IDENTIFIED_REVIEW'
        if status == 'INSUFFICIENT_GEOMETRY':
            reason = 'GEOMETRY_EXTRACTION_FAILED' if e.error else 'NO_HORIZONTAL_BASE_FACE'
        elif status == 'REVIEW_PATH_VIA_INTERSECTION':
            reason = 'INTERSECTION_REQUIRED_TO_REACH_FOUNDATION'
        elif status == 'NO_PATH_IDENTIFIED_REVIEW':
            reason = 'SUPPORT_PATH_TERMINATES' if supports[e.key] else 'NO_DIRECT_SUPPORT'
        elif unresolved:
            reason = 'UNRESOLVED_SUPPORT_BRANCH'
        else:
            reason = ''
        rows.append({'key': e.key, 'GlobalId': e.guid, 'type': e.ifc_class,
                     'name': e.name, 'storey': e.storey, 'status': status,
                     'bearing_path_status': 'NO_PATH_IDENTIFIED_REVIEW' if status == 'REVIEW_PATH_VIA_INTERSECTION' else status,
                     'review_reason': reason,
                     'direct_support_count': len(supports[e.key]),
                     'direct_geo_support_count': sum(by_key[key].terminal for key in supports[e.key]),
                     'supports': supports[e.key], 'example_path': path,
                     'review_supports': [x['lower'] for x in e.review_connections],
                     'review_example_path': review_path,
                     'review_path_intersections': review_links,
                     'unresolved_branch_ends': sorted(unresolved),
                     'missing_or_limited_information': e.issues,
                     'materials': e.materials, 'profiles': e.profiles,
                     'minimum_m': e.minimum, 'maximum_m': e.maximum})
    return rows


def _bounds(elements, source):
    items = [e for e in elements if e.source == source and e.minimum is not None and not e.error]
    return None if not items else {
        'minimum_m': np.min([e.minimum for e in items], axis=0).tolist(),
        'maximum_m': np.max([e.maximum for e in items], axis=0).tolist()}


def _csv(path, rows, fields):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(row[k], ensure_ascii=False) if isinstance(row.get(k), (list, dict))
                             else row.get(k, '') for k in fields})


def COMM_results(elements, edges, rows, config, output):
    """Write traceable JSON/CSV outputs and a concise human-readable report."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    bounds = {source: _bounds(elements, source) for source in ('STR', 'GEO')}
    counts = dict(Counter(r['status'] for r in rows))
    review_edges = [edge for e in elements for edge in e.review_connections]
    failures = [{'model': e.source, 'GlobalId': e.guid, 'name': e.name,
                 'type': e.ifc_class, 'error': e.error} for e in elements if e.error]
    issues = [row for row in rows if row['review_reason']]
    reasons = dict(Counter(row['review_reason'] for row in issues))
    summary = {'tool': 'IFC potential geometric load-path screening',
               'method_version': '3.0-review-diagnostics',
               'ifcopenshell_version': ifcopenshell.version,
               'tolerance_m': config['tolerance_m'], 'counts': counts,
               'foundation_selection_note': config.get('foundation_selection_note', ''),
               'element_counts': {s: dict(Counter(e.ifc_class for e in elements if e.source == s))
                                  for s in ('STR', 'GEO')},
               'foundation_terminals': sum(e.terminal for e in elements),
               'connections': len(edges), 'bounds': bounds,
               'review_intersections': len(review_edges),
               'geometry_failures': len(failures),
               'review_reasons': reasons,
               'review_elements_by_type': dict(Counter(row['type'] for row in issues)),
               'limitations': [
                   'Foundation terminal identities are provisional project assumptions.',
                   'Global placements are used; CRS/map conversions are not automatically reconciled.',
                   'Bearing paths use horizontal extreme base/top faces; STR beam/slab intersections with lower STR columns/walls form a separate review scenario.',
                   'Detected intersections may be joints or modelling clashes; they are not accepted bearing connections.',
                   'Side connections, hangers and stepped/sloping interfaces may still be missed.',
                   'Open gaps above tolerance are never bridged.',
                   'Tolerance is an unvalidated screening parameter, not a code requirement.',
                   'At least one path is enough for POTENTIAL_PATH_FOUND; all required bearings are not verified.',
                   'A missing path is unresolved evidence, not proof of a structural defect.',
                   'No load distribution, capacity, connection resistance or soil assessment is performed.']}
    (output / 'results.json').write_text(json.dumps({'summary': summary, 'elements': rows,
                                                  'connections': edges,
                                                  'review_connections': review_edges,
                                                  'geometry_failures': failures}, indent=2, ensure_ascii=False), encoding='utf-8')
    _csv(output / 'elements.csv', rows, list(rows[0]) if rows else ['GlobalId', 'status'])
    _csv(output / 'connections.csv', edges, ['upper', 'lower', 'vertical_gap_m', 'horizontal_gap_m',
                                           'overlap_area_m2', 'contact',
                                           'overlap_ratio_of_smaller_face'])
    _csv(output / 'load_path_issues.csv', issues,
         ['GlobalId', 'name', 'type', 'storey', 'status', 'review_reason',
          'direct_support_count', 'direct_geo_support_count', 'unresolved_branch_ends',
          'review_path_intersections', 'missing_or_limited_information'])
    _csv(output / 'geometry_failures.csv', failures, ['model', 'GlobalId', 'name', 'type', 'error'])
    _csv(output / 'review_connections.csv', review_edges,
         ['upper', 'lower', 'contact', 'vertical_gap_m', 'bbox_vertical_overlap_m',
          'intersection_evidence', 'used_in_bearing_graph', 'reason'])
    foundation_rows = [{'GlobalId': e.guid, 'type': e.ifc_class, 'name': e.name,
                        'included': e.terminal, 'basis': e.terminal_basis,
                        'minimum_m': e.minimum, 'maximum_m': e.maximum}
                       for e in elements if e.source == 'GEO']
    _csv(output / 'foundation_inventory.csv', foundation_rows,
         ['GlobalId', 'type', 'name', 'included', 'basis', 'minimum_m', 'maximum_m'])
    # Nearest eligible support in plan, regardless of elevation gap: diagnostic only.
    diagnostics = []
    bearing_pairs = {(edge['upper'], edge['lower']) for edge in edges}
    valid = [e for e in elements if not e.error and e.minimum is not None]
    for e in valid:
        if e.source != 'STR' or e.bottom is None or e.bottom.is_empty:
            continue
        candidates = []
        for lower in valid:
            if lower.key == e.key or lower.top is None or lower.top.is_empty:
                continue
            if lower.source == 'GEO' and not lower.terminal:
                continue
            if lower.maximum[2] > e.minimum[2] + EPS:
                continue
            if any(e.maximum[i] < lower.minimum[i] or lower.maximum[i] < e.minimum[i]
                   for i in (0, 1)):
                continue
            if e.bottom.intersection(lower.top).area > EPS ** 2:
                candidates.append((e.minimum[2] - lower.maximum[2], lower.key))
        if candidates:
            gap, lower_key = min(candidates)
            diagnostics.append({'element': e.key, 'nearest_below_in_plan': lower_key,
                                'vertical_gap_m': round(gap, 8), 'used_as_connection':
                                (e.key, lower_key) in bearing_pairs})
    _csv(output / 'nearest_below.csv', diagnostics,
         ['element', 'nearest_below_in_plan', 'vertical_gap_m', 'used_as_connection'])
    report = ['# Model screening results', '',
              f"STR elements: {len(rows)}. GEO candidates: {len(foundation_rows)}.",
              f"Provisional terminals: {summary['foundation_terminals']}. Connections: {len(edges)}.",
              f"Tolerance: {config['tolerance_m']} m. Geometry failures: {summary['geometry_failures']}.", '',
              f"Separately recorded intersections requiring review: {len(review_edges)}.", '',
              '| Status | Count |', '|---|---:|']
    report += [f'| {k} | {v} |' for k, v in sorted(counts.items())]
    if reasons:
        report += ['', '## Review reasons', '', '| Reason | Count |', '|---|---:|']
        report += [f'| {reason} | {count} |' for reason, count in sorted(reasons.items())]
    report += ['', '## Interpretation', '',
               'These are potential geometric paths to the listed foundation candidates. '
               'No result establishes structural safety. Unresolved paths require model and engineering review.',
               'REVIEW_PATH_VIA_INTERSECTION means that a path exists only in the review scenario. '
               'Its example_path remains empty; review_example_path lists the scenario and '
               'review_path_intersections identifies the unverified links. '
               'supports and connections retain the original bearing rule.',
               '', '## Limits and assumptions', '']
    report += ['- ' + item for item in summary['limitations']]
    (output / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    return summary


def analyse(str_model, geo_model, config):
    """Internal analysis pipeline; retains geometry for diagnostic file generation."""
    elements = CAPT_elements(str_model, 'STR') + CAPT_elements(geo_model, 'GEO')
    if len({e.key for e in elements}) != len(elements):
        raise ValueError('Duplicate GlobalIds within an input model')
    bounds = {s: _bounds(elements, s) for s in ('STR', 'GEO')}
    if any(b is None for b in bounds.values()):
        raise ValueError('One model has no usable relevant geometry')
    if any(bounds['STR']['maximum_m'][i] < bounds['GEO']['minimum_m'][i] or
           bounds['GEO']['maximum_m'][i] < bounds['STR']['minimum_m'][i] for i in (0, 1)):
        raise ValueError('Model bounds do not overlap in plan: check coordinate alignment')
    # This is a necessary broad check only, not proof of coordinate alignment.
    mark_terminals(elements, config['foundation_ids'])
    if not any(e.terminal and e.minimum is not None and not e.error for e in elements):
        raise ValueError('No listed foundation candidate has usable geometry')
    edges = CONN_supports(elements, config['tolerance_m'])
    return elements, edges, CHEK_paths(elements, edges)


def CHEK_load_path(str_model, geo_model, config):
    """Manager entry point: opened models in, JSON-compatible results out; no writes."""
    elements, edges, rows = analyse(str_model, geo_model, config)
    return {'elements': rows, 'connections': edges,
            'review_connections': [x for e in elements for x in e.review_connections],
            'tolerance_m': config['tolerance_m'],
            'foundation_selection_note': config.get('foundation_selection_note', '')}
