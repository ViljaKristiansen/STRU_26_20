# A3 – Automating BIM Data Extraction with Python

**Group 20 – Structures**

## 1. Introduction

In this tutorial, we demonstrate how Python and IfcOpenShell can be used to extract information from an IFC model.

Instead of manually searching through a BIM model, we can use a short Python script to identify structural elements, count them, and retrieve their information.

We learned this approach while developing the Capture stage of our A4 load-path screening tool, where structural elements must be identified before their possible connections can be investigated.

The tutorial is aimed at students with little or no experience using Python for BIM.

## 2. Learning Objectives

After completing this tutorial, you should be able to:

- Open an IFC model using Python and IfcOpenShell.
- Retrieve structural elements by IFC class.
- Count the retrieved elements.
- Extract their names and GlobalIds.
- Modify the script to investigate another element type.

**BIM role:** OpenBIM Analyst

**Target level:** Beginner in Python-based IFC data extraction. The corresponding course role learning level must be confirmed against the course role description.

**Focus area:** Structures

## 3. Requirements and Setup

Before starting, you need:

- Python installed on your computer.
- VS Code with the Python extension, or another Python editor.
- The tutorial script, `main.py`.
- An IFC model.

### Prepare your folder

1. Create a folder anywhere on your computer.
2. Download `main.py` from this tutorial and place it in the folder.
3. Place your IFC model in the same folder.
4. Open the folder in VS Code using **File → Open Folder**.

The folder can have any name. You do not need our A3 or A4 project structure.

For this example, we use `26-06-D-STR.ifc`, which course participants can obtain from the course model files. The model is not included in this repository.

### Install IfcOpenShell

In VS Code, select **Terminal → New Terminal** and run:

```powershell
python -m pip install ifcopenshell
```

If IfcOpenShell is already installed in the Python environment you are using, you can continue.

## 4. Python Tutorial

Open `main.py`. The script should contain:

```python
from pathlib import Path
import ifcopenshell

# Enter the filename of your IFC model
ifc_filename = "26-06-D-STR.ifc"

# Open the model stored beside this script
model_path = Path(__file__).resolve().parent / ifc_filename
model = ifcopenshell.open(str(model_path))

# Find all columns
columns = model.by_type("IfcColumn")

# Print the total and information about the first five columns
print("Number of columns:", len(columns))

for column in columns[:5]:
    print("Name:", column.Name)
    print("GlobalId:", column.GlobalId)
    print()
```

If you use a different IFC model, change `ifc_filename` to its exact filename, including the `.ifc` extension.

The script finds the model relative to its own location. It therefore works without a personal file path, provided the script and model are stored in the same folder.

### How does the code work?

| Code | Explanation |
|---|---|
| `from pathlib import Path` | Imports a tool for working with file paths. |
| `import ifcopenshell` | Imports the library used to read IFC files. |
| `ifc_filename` | Stores the filename of the model to open. |
| `Path(__file__).resolve().parent` | Finds the folder containing this script. |
| `... / ifc_filename` | Builds the path to the model in that folder. |
| `ifcopenshell.open(str(model_path))` | Opens the IFC model using the path as text. |
| `model.by_type("IfcColumn")` | Retrieves objects classified as IfcColumn. |
| `len(columns)` | Counts the retrieved objects. |
| `columns[:5]` | Selects the first five columns for printing. |
| `for column in columns[:5]:` | Repeats the indented instructions for each selected column. |
| `column.Name` | Retrieves the column's name. |
| `column.GlobalId` | Retrieves its unique IFC identifier. |
| `print()` | Adds a blank line between elements. |

All retrieved columns are counted. Only the first five have their details printed.

## 5. Run the Script

1. Save `main.py` using **Ctrl + S**.
2. Make sure the terminal is open in the folder containing `main.py`.
3. Run:

```powershell
python main.py
```

### Expected Output

For the course STR model used in our test, the output begins with:

```text
Number of columns: 278
```

The script then prints the name and GlobalId of the first five columns.

Names, identifiers and counts depend on the model and its version. If you use another model, your results may differ.

A GlobalId allows an element to be identified in IFC-based workflows, for example when referring to an element in a checking result.

### Understanding the Result

The number represents objects classified as `IfcColumn` in the IFC model.

It does not verify that every physical column was exported or correctly classified. The script extracts model information; it does not check structural capacity or load paths.

## 6. Try It Yourself

### Exercise: Extract beams

1. Change `"IfcColumn"` to `"IfcBeam"`.
2. Rename the variable `columns` to `beams` everywhere it appears.
3. Change `"Number of columns:"` to `"Number of beams:"`.
4. Save the script and run it again.

Your extraction and printing section should now be:

```python
# Find all beams
beams = model.by_type("IfcBeam")

# Print the total and information about the first five beams
print("Number of beams:", len(beams))

for beam in beams[:5]:
    print("Name:", beam.Name)
    print("GlobalId:", beam.GlobalId)
    print()
```

How many beam objects does your model contain?

### Further practice: Extract slabs

Adapt the script again using `"IfcSlab"`.

Update the variable names and output label to match the element type.

### Check your understanding

- What does `by_type()` select?
- Why are only five elements printed even though the count is larger?
- What would a count of zero tell you?
- What must you change to use another IFC model?

## 7. Troubleshooting

| Problem | Suggested solution |
|---|---|
| `python` is not recognised | Check that Python is installed and available in your terminal. Restart VS Code after installation. |
| `ModuleNotFoundError: No module named 'ifcopenshell'` | Run `python -m pip install ifcopenshell` using the same Python environment used to run the script. |
| Python cannot find `main.py` | Open your tutorial folder using **File → Open Folder**, then open a new terminal there. |
| The IFC model cannot be opened | Check that it is in the same folder as `main.py` and that its filename matches `ifc_filename`. |
| No output appears | Save the script with **Ctrl + S** and run it again. |
| The count is zero | The model may contain no objects classified under the selected IFC class. Check the class spelling and model contents. |
| A name is printed as `None` | The element does not have a Name value assigned. |

## 8. Video Tutorial

The accompanying video demonstrates how to prepare the files, run the script, understand the output, and adapt the code to another element type.

**Video link:** To be added before submission.

## 9. Peer Testing and Feedback

Ask another group to follow the tutorial and complete the beam exercise.

Collect feedback on:

- Whether the setup and instructions were clear.
- Whether the script ran successfully.
- Whether the participant understood the count, Name and GlobalId.
- Whether they could adapt the script to beams.
- Any improvements needed.

Record the testing group, date, feedback and changes made. Keep this information for the A5 reflection.

## 10. Summary

**Automating BIM Data Extraction with Python**

This tutorial demonstrates how to use Python and IfcOpenShell to extract structural information from an IFC model. Participants learn to identify and count building elements, retrieve their names and GlobalIds, and adapt the script to other element types.
