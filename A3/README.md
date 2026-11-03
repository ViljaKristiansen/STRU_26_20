# A3 – Automating BIM Data Extraction with Python

## 1. Introduction

In this tutorial, we demonstrate how Python and IfcOpenShell can be used to extract information from an IFC model.

Instead of manually searching through a BIM model, we can use a short Python script to automatically identify structural elements and retrieve their information.

The tutorial is aimed at students with little or no experience using Python for BIM.

## 2. Learning Objectives

After completing this tutorial, you should be able to:

- Open an IFC model using Python.
- Find structural elements using IfcOpenShell.
- Extract information such as element names and GlobalIds.
- Understand how Python can automate simple BIM tasks.

**BIM role:** OpenBIM Analyst

**Learning level:** Level 1 – Introduction to Python-based IFC data extraction.

## 3. Requirements

Before starting, you need:

- Python
- VS Code (or another Python editor)
- IfcOpenShell
- An IFC model (`26-06-D-STR.ifc`)

Install IfcOpenShell by running this command in the terminal:

```bash
pip install ifcopenshell
```

Make sure the IFC file is located in the same working directory as your Python script.

## 4. Python Tutorial

The following code extracts information about structural columns from an IFC model.

```python
import ifcopenshell

# Open the IFC model
model = ifcopenshell.open("26-06-D-STR.ifc")

# Find all columns
columns = model.by_type("IfcColumn")

# Print the number of columns
print("Number of columns:", len(columns))

# Print the name and GlobalId of the first five columns
for column in columns[:5]:
    print("Name:", column.Name)
    print("GlobalId:", column.GlobalId)
    print()
```

### How does the code work?

| Code | Explanation |
|---|---|
| `import ifcopenshell` | Imports the library used to read IFC files. |
| `ifcopenshell.open()` | Opens the IFC model. |
| `model.by_type("IfcColumn")` | Finds all columns in the model. |
| `len(columns)` | Counts the columns. |
| `columns[:5]` | Selects the first five columns. |
| `column.Name` | Retrieves the column name. |
| `column.GlobalId` | Retrieves its unique IFC identifier. |

### Expected Output

The output will look similar to this:

```text
Number of columns: 278

Name: Column 1
GlobalId: ...

Name: Column 2
GlobalId: ...
```

The exact names and identifiers depend on the IFC model.

## 5. Try It Yourself

Now try modifying the code:

1. Change `"IfcColumn"` to `"IfcBeam"`.
2. Run the script again.
3. How many beams are in the model?
4. Try extracting slabs using `"IfcSlab"`.

This demonstrates how the same code can be used to extract information about different building elements.

## 6. Video Tutorial

A short video demonstrates how to run the code in VS Code and explains the results.

**Video:** [Add video link here]

## 7. Summary

**Extracting Structural BIM Information Using Python and IfcOpenShell**

This tutorial demonstrates how to use Python and IfcOpenShell to extract structural information from an IFC model. Students learn how to identify building elements, count them, and retrieve their names and unique identifiers.
