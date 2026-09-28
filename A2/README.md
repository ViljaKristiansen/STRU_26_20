## A2a – About our group

**Python coding level:** 6  
Both group members rated their confidence in coding Python as 3 – Agree.

**Focus area:** Structures  
**Role:** Analyst

## A2b – Identify Claim

**Selected report:** 26-06-D-STR-Anon.pdf   
**Selected building:** Building 308 

### Claim

In Section 2.1, *Vertical*, on page 2 of Structural Report #2606, it is stated that the new columns are positioned to align with existing load-bearing elements, allowing loads to be transferred through the existing structure towards the foundation.

Based on this statement, the selected claim is:

> **The new structural system is intended to provide a continuous vertical load path through the new and existing load-bearing elements towards the foundation.**


### Motivation

We will investigate whether a continuous potential geometric load path can be identified through slabs, beams, columns and walls on successive storeys in the IFC model.

If a continuous path cannot be identified, the location will be flagged for further structural review. The check does not verify structural capacity, but identifies possible discontinuities and missing information in the model.

This claim was selected because Building 308 combines a new timber structure with an existing concrete structure, making the load transfer between new and existing elements particularly important.   

## A2c – Use Case

### How would we check this claim?

The structural and GEO IFC models are analysed to identify possible vertical load paths through the structural system. Relevant structural elements, such as slabs, beams, columns and walls, are identified and their spatial relationships are analysed across the two models.

These relationships can be represented as a structural graph, where structural elements are nodes and potential support relationships are connections. The graph can then be used to investigate the question:

> **Is there an uninterrupted structural support chain from this element to the foundation?**

If no continuous support chain can be identified, the element is flagged as a potential discontinuity for further review by a structural engineer.

In addition, the available information for the elements in the load path is checked to determine whether the model contains the information required for a subsequent structural capacity assessment. This includes geometry, dimensions, material and cross-section information.

The use case does not perform a structural capacity calculation.

### When would this claim need to be checked?

The check should be performed during the structural design and coordination process and repeated when significant changes are made to the structural model.

It can be particularly useful when new structural elements interact with an existing structure, as changes in element position or geometry may affect the intended vertical load path.

### What information does this claim rely on?

The check relies primarily on information contained in the structural and GEO
IFC models, including:

- Structural elements such as slabs, beams, columns and walls
- Foundation-related elements
- Building storeys
- Element geometry and position
- Spatial relationships between structural elements
- Element GlobalId
- Material information
- Cross-section and dimensions

### Phase

**Design**

### BIM purpose

**Analyse**

The BIM model is analysed to identify potential vertical load paths,
discontinuities and the availability of information required for further
structural analysis.

### BIM Use Case

**Design review / model checking**

The use case systematically analyses the structural IFC model to identify
possible load paths and conditions requiring further engineering review. It
also evaluates whether the model contains sufficient structural information
for a subsequent capacity assessment.

### BPMN diagram

![BPMN diagram](IMG/diagramv3.svg)

## A2d – Tool idea

The proposed tool covers the automated IFC checking part of the overall use case.

The tool reads structural data from the structural and GEO IFC models, creates a structural support graph and traces potential vertical load paths towards the
foundation. It also checks whether the required structural information is available for a subsequent capacity assessment.

The tool generates a results report containing identified load paths, potential
load-path discontinuities and missing information.

Structural engineering judgement, capacity verification and decisions regarding
model changes remain outside the scope of the tool.

### Tool Scope Diagram

![BPMN diagram](IMG/diagramhighlights.svg)

## A2e – Tool idea

### IFC Load Path Checker

The proposed tool is a Python-based OpenBIM tool developed with IfcOpenShell. Its purpose is to identify potential vertical load paths across structural and
GEO IFC models and highlight elements that may require further review by a structural engineer.

The tool uses two IFC models as input: the structural IFC model
(`26-06-D-STR.ifc`) and the GEO IFC model (`26-06-D-GEO.ifc`).

Relevant elements include:

- `IfcSlab`
- `IfcBeam`
- `IfcColumn`
- `IfcWall`
- `IfcBuildingStorey`

The geometry, placement, dimensions, material information and `GlobalId` of the elements are extracted. Geometric relationships and a defined tolerance are then used to identify potential support relationships between the elements.

The support relationships are represented as a directed graph. The tool traces potential load paths downwards through slabs, beams, columns and walls. The
structural IFC model provides the main structural system, while foundation-related elements are identified in the GEO IFC model. A path is considered complete
when a continuous potential support chain can be identified towards these foundation-related elements.

Elements without a continuous potential load path are flagged as possible load-path discontinuities. The tool also checks whether information required for a later structural capacity assessment is available, such as element dimensions, materials and cross-sections.

The results report includes:

- Element type and `GlobalId`
- Associated building storey
- Potential supporting elements
- Load-path status
- Identified discontinuities
- Missing structural information

The tool performs a geometric and information-based model check. It does not calculate structural capacity or verify that a load path is structurally sufficient. The final assessment must therefore be performed by a structural engineer.

### Business value

The tool can reduce the time required for manual review of structural IFC models. Potential discontinuities and missing information can be identified earlier in the design process, reducing the risk of late design changes, coordination problems and additional costs.

Because the tool uses IFC and IfcOpenShell, it is independent of specific modelling software and can be reused in different OpenBIM projects. The results are traceable through the `GlobalId` of each element, which can improve communication between BIM modellers and structural engineers.

### Societal value

Earlier identification of possible discontinuities can support improved structural quality and safety. The tool does not replace engineering calculations, but it helps structural engineers identify areas requiring additional attention.

Detecting modelling problems early may also reduce unnecessary redesign, construction rework and material waste. This is particularly relevant for renovation projects such as Building 308, where new structural elements must interact with an existing structural system.

### BPMN diagram

The BPMN diagram below presents the internal workflow of the proposed Python/IfcOpenShell tool.
![BPMN diagram for the IFC Load Path Checker](IMG/diagram.svg)

## A2f – Information Requirements

The tool requires geometric and semantic information from both the structural
IFC model (`26-06-D-STR.ifc`) and the GEO IFC model (`26-06-D-GEO.ifc`) to
construct the structural support graph, trace vertical load paths and assess
whether relevant structural model information is available for subsequent
structural calculations.

Both IFC models were investigated using IfcOpenShell to determine which of the
required information is available.

| Information required | Source | Where in IFC? | In the model? | Know how to extract with IfcOpenShell? | What do we need to learn? |
|---|---|---|---|---|---|
| Structural columns | STR | `IfcColumn` | Yes – 278 | Yes | - |
| Structural beams | STR | `IfcBeam` | Yes – 272 | Yes | - |
| Structural slabs | STR | `IfcSlab` | Yes – 157 | Yes | - |
| Structural walls | STR | `IfcWall` | Yes – 93 | Yes | - |
| Foundation-related elements | GEO | `IfcWall` | Yes – 18 identified by foundation-related names | Yes | Determine how these elements connect geometrically to the structural model |
| Building storeys | STR / GEO | `IfcBuildingStorey` / spatial containment | Yes – 6 in each model | Yes | - |
| GlobalId | STR / GEO | IFC element attribute | Yes | Yes | - |
| Element position | STR / GEO | `ObjectPlacement` / geometry | Yes | Partly | Compare global positions consistently across the two models |
| Element geometry and dimensions | STR / GEO | `Representation` / geometry | Yes | Partly | Determine element boundaries and geometric overlap |
| Material | STR / GEO | `IfcRelAssociatesMaterial` | Yes | Partly | Extract and interpret material information consistently |
| Cross-section / profile | STR | `IfcProfileDef`, element types and geometry | Partly – 475 profiles are present | Partly | Determine how profile dimensions are represented and extract them consistently |tructural level |

## A2g – Software Licence

### GPL-3.0

We have chosen the GNU General Public License v3.0 (GPL-3.0) for our project.

The project contains source code and is intended to be open and reusable.
GPL-3.0 allows others to use, modify and redistribute the code, while requiring
distributed modified versions to remain available under the same open-source
licence.

This is suitable for our OpenBIM tool because it supports open development,
reuse and further improvement of the code.
