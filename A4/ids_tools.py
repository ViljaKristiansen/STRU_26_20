"""Create and validate the semantic IDS preflight. Geometry is checked separately."""
import argparse
import json
from pathlib import Path
import ifcopenshell
from ifctester import ids


def create(folder):
    for source, kinds in [('STR', ['IFCCOLUMN','IFCBEAM','IFCSLAB','IFCWALL']),
                          ('GEO', ['IFCCOLUMN','IFCWALL'])]:
        document = ids.Ids(title=f'Building 308 {source} load-path information',
                           description='Semantic preflight only. Runtime geometry and coordinate checks are also required.',
                           purpose='Information availability for geometric screening')
        for kind in kinds:
            spec = ids.Specification(name=f'{source} {kind}: identity, name, material and storey',
                                     minOccurs=1, ifcVersion=['IFC4'])
            spec.applicability.append(ids.Entity(name=kind))
            spec.requirements.extend([ids.Attribute(name='GlobalId'), ids.Attribute(name='Name'),
                                      ids.Material(), ids.PartOf(name='IFCBUILDINGSTOREY',
                                                               relation='IFCRELCONTAINEDINSPATIALSTRUCTURE')])
            document.specifications.append(spec)
        path = folder / f'{source.lower()}_requirements.ids'
        if not document.to_xml(str(path)):
            raise RuntimeError(f'Invalid IDS generated: {path}')


def validate(folder, str_path, geo_path, output):
    results = []
    for source, model_path in [('STR',str_path), ('GEO',geo_path)]:
        document = ids.open(str(folder / f'{source.lower()}_requirements.ids'), validate=True)
        document.validate(ifcopenshell.open(str(model_path)))
        for spec in document.specifications:
            results.append({'model': source, 'specification': spec.name, 'passed': spec.status,
                            'applicable_elements': len(spec.applicable_entities),
                            'failed_elements': len(spec.failed_entities)})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true')
    parser.add_argument('--str', dest='str_path', type=Path)
    parser.add_argument('--geo', dest='geo_path', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    if args.create:
        create(here)
    else:
        if not args.str_path or not args.geo_path:
            parser.error('--str and --geo are required for validation')
        validate(here,args.str_path,args.geo_path,here / 'output' / 'ids_results.json')
