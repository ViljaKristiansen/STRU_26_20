# STRU_26_20

# A1 – Forensic BIM

**Group 20 – Structures**

## Project claim

We investigated whether structural information in the client report for **Group 26-1** corresponds with the IFC model using Python and IfcOpenShell.

Our focus area was the structural system of the building.

Three issues were investigated:

1. Beam span
2. Number and classification of beams
3. Number of floors

## 1. Beam span

**Source:** Client report for Group 26-1, page 10 - section 3.1 *Auditoriums* .

**Report:** The primary beams in the auditorium span approximately 12.8 m between columns.

**IFC:** Only two objects classified as `IfcBeam` were found. Their horizontal geometric extents are approximately 64.08 m and 64.04 m.

**Finding:** The IFC beam geometry does not correspond directly to the 12.8 m structural span stated in the report.

**Likely cause:** This is most likely a modelling or checking-method issue, since one continuous IFC object can extend across several structural spans.

**Possible solution:** Review how the beams are divided and classified in the IFC model. The checking method could also be improved by measuring the distance between beam supports instead of using the total geometric extent of each beam object.

## 2. Number and classification of beams

**Source:** Client report for Group 26-1, page 10 - section 3.1 *Auditoriums*.

**Report:** The building is described as a reinforced-concrete beam-and-slab structure with primary and secondary beams.

**IFC:** Only 2 objects are classified as `IfcBeam`, while 951 objects are classified as `IfcMember`.

**Finding:** The low number of `IfcBeam` objects does not appear to represent the complete beam system described in the report. Structural elements that function as beams may instead have been classified as `IfcMember`.

**Likely cause:** This is most likely a modelling or IFC export issue caused by the classification or export mapping of structural elements. It does not necessarily mean that the geometry is missing.

**Possible solution:** Review the IFC classifications and export mapping. Elements that function as beams should be classified consistently as `IfcBeam`.

## 3. Number of floors

**Source:** Client report for Group 26-1, page 10 section 3 *Structures*.

**Report:** The building is described as having two main floors.

**IFC:** The model contains 6 `IfcBuildingStorey` objects.

**Finding:** The number of IFC storeys does not correspond directly to the number of main floors described in the report.

**Likely cause:** This is most likely caused by differences in how floors and modelling levels are defined. Some of the `IfcBuildingStorey` objects may represent a basement, roof level, intermediate level or another modelling level rather than a main occupied floor.

**Possible solution:** Review the names, elevations and intended purposes of the `IfcBuildingStorey` objects. Main floors should be clearly distinguished from other modelling levels.

## Conclusion

The checks show differences between the client report for Group 26-1 and the IFC model concerning beam geometry, element classification and spatial structure.

The findings do not necessarily represent design errors. They demonstrate that IFC geometry, classification and spatial structure must be interpreted carefully before deciding whether an issue originates from the design, the model or the checking method.

## Tools

Python · IfcOpenShell · IFC4X3
