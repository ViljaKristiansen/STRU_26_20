from pathlib import Path
import ifcopenshell

# Enter the filename of your IFC model - here we use the STR model as example
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
