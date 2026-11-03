import ifcopenshell

# Open the IFC model
model = ifcopenshell.open(
    r"C:\Users\Vilja\OneDrive - Danmarks Tekniske Universitet\STRU_26_20\ifc filer\26-06-D-STR.ifc"
)

# Find all columns
columns = model.by_type("IfcColumn")

# Print the number of columns
print("Number of columns:", len(columns))

# Print the name and GlobalId of the first five columns
for column in columns[:5]:
    print("Name:", column.Name)
    print("GlobalId:", column.GlobalId)
    print()
