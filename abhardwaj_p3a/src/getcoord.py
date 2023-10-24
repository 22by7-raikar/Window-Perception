import bpy
import bmesh

# Retrieve the object by name
obj = bpy.data.objects.get("Plane.001")

if obj and obj.type == 'MESH':  # Ensure the object exists and is a mesh
    
    # Create a BMesh instance and ensure it's in object mode
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(obj.matrix_world)  # Convert local to global coordinates
    
    # Print global coordinates of each vertex
    for v in bm.verts:
        print(f"Global coordinates of vertex {v.index} in object {obj.name}: {v.co}")
    
    bm.free()  # Free the BMesh to save memory
else:
    print("Object 'Plane.001' not found or it's not a mesh.")
