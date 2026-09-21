import ifcopenshell
import ifcopenshell.geom
import math
from pathlib import Path

IFC_PATH = Path(__file__).parent / "B308X.ifc"
ifc = ifcopenshell.open(str(IFC_PATH))

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

beams = ifc.by_type("IfcBeam")
members = ifc.by_type("IfcMember")
storeys = ifc.by_type("IfcBuildingStorey")

print(f"Number of beams: {len(beams)}")
print(f"Number of members: {len(members)}")
print(f"Number of storeys: {len(storeys)}")

for i, beam in enumerate(beams, 1):
    shape = ifcopenshell.geom.create_shape(settings, beam)
    verts = shape.geometry.verts

    xs = verts[0::3]
    ys = verts[1::3]

    x = max(xs) - min(xs)
    y = max(ys) - min(ys)

    length = math.sqrt(x**2 + y**2)

    print(f"Beam {i}: {length:.3f} m")

for storey in storeys:
    print(f"{storey.Name}: {storey.Elevation}")
