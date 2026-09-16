# STRU_26_20

# A1 – Forensic BIM
**Group 20 – Structures**

## Project claim

We investigated whether structural information in the client report corresponds with the IFC model using Python and IfcOpenShell.

Three issues were investigated:
1. Beam span
2. Number of beams
3. Number of floors

## 1. Beam span

**Report:** The primary beams in the auditorium span approximately 12.8 m between columns.

**IFC:** Only two IfcBeam objects were found. Their horizontal geometric extents are approximately 64.08 m and 64.04 m.

**Finding:** The IFC beam geometry does not correspond directly to the 12.8 m structural span stated in the report. This may be a modelling issue, since one continuous IFC object can extend across several structural spans.

**Possible solution:** Review how the beams are divided and classified in the IFC model.

## 2. Number of beams

**Report:** The building is described as a reinforced-concrete beam-and-slab structure with primary and secondary beams.

**IFC:** Only 2 objects are classified as IfcBeam, while 951 objects are classified as IfcMember.

**Finding:** The low number of IfcBeam objects suggests a classification/export issue or perhaps missing geometry.

**Possible solution:** Review the IFC classifications and export mapping of structural members.

## 3. Number of floors

**Report:** The building is described as having two main floors.

**IFC:** The model contains 6 IfcBuildingStorey objects.

**Finding:** The number of IFC storeys does not correspond to the number of main floors. Some may represent basement, roof orother modelling levels.

**Possible solution:** Review the naming and purpose of the IfcBuildingStorey objects.

## Conclusion

The checks show differences between the structural report and the IFC model. They also demonstrate that IFC geometry, classification and spatial structure must be interpreted before deciding whether an issue comes from the design, model or checking method.

## Tools
Python · IfcOpenShell · IFC4X3
