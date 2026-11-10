# A4 – IFC Load Path Checker

**Group 20 – Structures | Building 308 | Analyst**

## About the tool

### Problem / claim

The tool addresses the need to check whether structural elements in the proposed design have a potential continuous vertical support path towards the foundation system. Missing or unclear geometric connections between slabs, beams, columns, walls and foundation candidates can be difficult to identify by manually inspecting separate BIM models.

The tool performs **geometric screening**, not structural verification. A detected path is not proof of load transfer, structural capacity or safety; an undetected path is not proof of a defect.

### Where the problem was found

The use case was identified in our [A2 Use Case Analysis](../A2/README.md), based on **Structural Report #2606, Section 2.1, “Vertical”, page 2**, for Building 308. The analysis concerns coordination of the structural (STR) and geotechnical/foundation (GEO) IFC models.

### Description of the tool

The Python tool uses **IfcOpenShell**, NumPy and Shapely to examine two IFC4 models. Its workflow follows four steps:

1. **CAPT – Capture:** Read `IfcColumn`, `IfcBeam`, `IfcSlab` and `IfcWall` from STR, and `IfcColumn`, `IfcWall`, `IfcFooting` and `IfcPile` from GEO. Extract GlobalIds, names, storey associations, available materials/profiles and world-space geometry.
2. **CONN – Connect:** Identify potential upper-to-lower bearing contacts using vertical proximity and actual horizontal mesh-face overlap. Separately record selected geometric intersections between STR beams/slabs and lower STR columns/walls for manual review.
3. **CHEK – Check:** Search the directed support graph for possible paths from STR elements to explicitly listed GEO foundation candidates. Record unresolved branches and distinguish paths that exist only when unverified intersections are considered.
4. **COMM – Communicate:** Export traceable CSV and JSON results and a short Markdown report, including element statuses, review reasons, connections and limitations.

The separate IDS preflight checks the presence of selected IFC classes and semantic information (identity, name, material and storey containment). It does not check structural connections.

### Instructions to run the tool

**Requirements:** Python 3.11 or 3.12 and the packages listed in `requirements.txt`.

From the `A4` folder, install dependencies:

```bash
python -m pip install -r requirements.txt
```

Place the two input models in the folder, or provide their full paths. To run the geometric analysis:

```bash
python main.py --str "26-06-D-STR.ifc" --geo "26-06-D-GEO.ifc"
```

To validate the existing IDS files:

```bash
python ids_tools.py --str "26-06-D-STR.ifc" --geo "26-06-D-GEO.ifc"
```

The IDS files can be regenerated with `python ids_tools.py --create`, if necessary. Run the validation command afterwards.

The default screening tolerance is **0.02 m (20 mm)**, specified in `config.json`. An alternative tolerance and output folder can be selected, for example:

```bash
python main.py --str "26-06-D-STR.ifc" --geo "26-06-D-GEO.ifc" --tolerance 0.01 --output output_10mm
```

Outputs are saved in `output/` by default. Paths containing spaces should be enclosed in quotation marks. The IFC files can be kept outside GitHub and referenced using their local paths; the models are not required to be committed to the repository.

## Advanced Building Design

### Relevant design stage (A, B, C or D)

The tool is most useful during **Stages C and D**, when structural design information is being coordinated and developed in more detail. It can highlight possible missing support paths or unclear geometric intersections before further detailing and engineering review. It may also support earlier model coordination when sufficiently developed IFC models are available. The stage assignment is an intended use of this tool, not a claim that the geometric check replaces stage-specific design verification.

### Potential users / subjects

- **Structural engineers / structural analysts:** Review potential vertical support chains and elements requiring further investigation.
- **BIM coordinators:** Identify geometric coordination issues between the STR and GEO models.
- **Foundation or geotechnical engineers:** Review whether the assumed foundation candidates and structural interfaces are consistent with the design documentation.
- **Design teams:** Use the exported GlobalIds and review lists to locate issues in their authoring or coordination software.

### Information required in the model

The tool needs:

- Two readable **IFC4** models representing the STR and GEO disciplines, with compatible global placements and geometry that can be processed by IfcOpenShell.
- Structural elements classified as the IFC types listed above, with usable geometric representations and `GlobalId` values.
- A consistent coordinate system and units; the tool uses world-space geometry in metres and checks broad plan overlap, but does not automatically align different coordinate reference systems.
- An explicit list of provisional GEO foundation-terminal `GlobalId`s in `config.json`, matched to the supplied GEO model.
- A screening tolerance in metres (`tolerance_m`).
- For the **IDS information check**, element names, material assignments and building-storey containment, in addition to identity and the relevant IFC classes.

The geometric path check can still report paths when some semantic metadata is missing; missing metadata is reported separately. The tool does not require loads, material strengths or section capacities because these are not assessed.

## Foundation selection and assumptions

`config.json` contains **227 provisional GEO foundation candidates**: 18 foundation-named GEO walls and 209 non-temporary GEO columns. Three objects named `T - Point (temporary)` are excluded. These are project-specific assumptions, **not independently verified foundation classifications**. Their roles must be checked against GEO documentation before engineering interpretation.

The file `foundation_inventory.csv` records all 230 GEO elements and which are included. If an expected foundation GlobalId is absent, the program raises an error instead of silently substituting another element.

## Coordinates and geometric method

Both supplied models declare millimetres. IfcOpenShell produces world-space geometry in metres with the current geometry settings; the mesh coordinates must not be scaled a second time. The models have broadly overlapping plan extents. STR geometry spans approximately Z = 40.00–57.25 m and GEO approximately Z = 38.40–40.70 m. Broad overlap is a necessary check, not proof of survey or coordinate accuracy.

Potential bearing contacts are determined from horizontal faces at the extreme bottom and top elevations, with a **20 mm provisional screening tolerance**. The program distinguishes face contacts from contacts within tolerance. A separate review scenario considers selected geometric intersections that may represent joints or modelling clashes; these intersections are **not** accepted as verified bearing connections.

The tolerance is not an Eurocode requirement or a calibrated connection acceptance criterion. Sloping/stepped interfaces, side bearings, hangers and other connection types may be missed.

## Output files

| File | Contents |
|---|---|
| `report.md` | Summary, status counts, review reasons, assumptions and limitations |
| `elements.csv` | STR elements, metadata, supports, paths and review statuses |
| `connections.csv` | Candidate bearing connections, gaps, overlap and contact classification |
| `review_connections.csv` | Selected geometric intersections requiring manual review |
| `load_path_issues.csv` | Flagged STR elements and reasons for review |
| `geometry_failures.csv` | Geometry extraction failures, if any |
| `foundation_inventory.csv` | All GEO candidates and provisional terminal selection |
| `nearest_below.csv` | Nearest eligible support below in plan, for diagnostics only |
| `results.json` | Full machine-readable geometric analysis results |
| `inputs.json` | Input filenames and SHA-256 hashes |
| `ids_results.json` | Results of the six semantic IDS specifications |

CSV fields containing lists are JSON-encoded. Output filenames are overwritten on subsequent runs in the same output directory.

## Status interpretation

| Status | Meaning |
|---|---|
| `POTENTIAL_PATH_FOUND` | At least one candidate bearing path reaches a listed GEO terminal; no unresolved branch was found in the generated support graph |
| `POTENTIAL_PATH_FOUND_WITH_UNRESOLVED_BRANCHES` | A candidate bearing path exists, but other generated branches terminate without a terminal |
| `REVIEW_PATH_VIA_INTERSECTION` | A path appears only in the separate scenario that includes unverified geometric intersections; manual review is necessary |
| `NO_PATH_IDENTIFIED_REVIEW` | No path was identified by either the bearing graph or the separate intersection-review scenario |
| `INSUFFICIENT_GEOMETRY` | The element could not be assessed using the required horizontal base-face method |

A positive status does **not** mean that all supports are sufficient or that the element is structurally safe. A negative status identifies an issue for review, not a confirmed structural defect.

## Tested model results

The latest completed run used the supplied STR and GEO models and the default **20 mm tolerance**.

| Status | STR elements |
|---|---:|
| `POTENTIAL_PATH_FOUND` | 109 |
| `POTENTIAL_PATH_FOUND_WITH_UNRESOLVED_BRANCHES` | 339 |
| `REVIEW_PATH_VIA_INTERSECTION` | 242 |
| `NO_PATH_IDENTIFIED_REVIEW` | 95 |
| `INSUFFICIENT_GEOMETRY` | 15 |
| **Total** | **800** |

The geometric analysis reported **1,494 candidate bearing connections**. The 15 insufficient-geometry cases refer to elements without a suitable horizontal bottom face for this method; they should not be confused with failed mesh extraction.

### IDS validation

All **six IDS specifications passed**, covering **1,030 applicable STR/GEO elements with zero failed elements**:

| Model | IFC class | Applicable | Failed |
|---|---|---:|---:|
| STR | IfcColumn | 278 | 0 |
| STR | IfcBeam | 272 | 0 |
| STR | IfcSlab | 157 | 0 |
| STR | IfcWall | 93 | 0 |
| GEO | IfcColumn | 212 | 0 |
| GEO | IfcWall | 18 | 0 |
| **Total** | | **1,030** | **0** |

These results confirm the specified semantic information checks for the supplied models, **not** the validity of geometric connections or structural capacity.

## Known limitations

- Foundation terminals are provisional project assumptions requiring verification.
- The method checks potential geometric continuity, not actual load distribution, connection resistance, material strength, foundation capacity or soil behaviour.
- Global placement consistency is assumed; automatic coordinate-system reconciliation is outside the scope.
- Only horizontal extreme faces are used for the bearing graph. Sloping/stepped geometry, side connections and some embedded joints may be missed.
- Mesh intersections are a separate **review** scenario and may indicate either intended connections or modelling clashes.
- A 20 mm tolerance can change the reported number of potential paths; it must not be tuned merely to improve the results.
- A missing geometric path is an unresolved modelling or coordination question, not proof of structural failure.

## Reuse by the manager group

The checker can be imported into another Python workflow without automatically writing files:

```python
import json
import ifcopenshell
from A4.load_path import CHEK_load_path

with open("A4/config.json", encoding="utf-8") as file:
    config = json.load(file)

str_model = ifcopenshell.open("C:/your/models/26-06-D-STR.ifc")
geo_model = ifcopenshell.open("C:/your/models/26-06-D-GEO.ifc")
results = CHEK_load_path(str_model, geo_model, config)
```

This example assumes the GitHub folder is named `A4` and the script is run from the repository root. The returned dictionary contains element results, candidate connections, review connections and configuration information. The `main.py` command-line entry point handles report generation.

## Licence

GPL-3.0, consistent with the selection in A2.
