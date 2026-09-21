## A2a – About our group

**Python coding level:** 6  
Both group members rated their confidence in coding Python as 3 – Agree.

**Focus area:** Structures  
**Role:** Analyst

## A2b - Identify claim

**Selected report:** Structural Report #2606  
**Selected building:** Building 308  
**Focus area:** Structures

**Claim from Structural Report #2606:**  
In the Structural Report for the transformation of Building 308, Section 2.1, *Vertical*, page 2, the following statement is made:

> “The new columns are positioned to align with existing load-bearing elements where possible, allowing additional loads to be transferred through the existing concrete structure down to the basement and foundation level.”

**Description of the claim:**  
Based on the statement in Structural Report #2606, we want to investigate whether the new columns in the IFC model of Building 308 are vertically aligned with columns on the storey below. Columns that do not overlap with a column below will be identified and flagged as potential discontinuities in the vertical load path.

A column that is not vertically aligned is not necessarily a structural error. The load may instead be transferred through a beam, wall or slab. The flagged areas must therefore be assessed further by a structural engineer.

**Justification for selecting the claim:**  
A clear vertical load path is important for transferring loads through the structure to the foundations. Misaligned columns may introduce concentrated forces or require additional transfer structures. Identifying these locations manually can be time-consuming, particularly in a large structural model.

The claim from Structural Report #2606 is suitable for an OpenBIM-based check because the IFC model can provide information about the columns, their storeys, positions and geometry. An automated check can help identify areas in Building 308 that require closer examination during the design and coordination process.
