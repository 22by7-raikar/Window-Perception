import os
import yaml
from scipy import io
import bpy

curr_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(curr_dir, 'configs/cfg.yaml')) as file:
    try:
        print(curr_dir)
        cfg = yaml.safe_load(file)

    except yaml.YAMLError as exception:
        print(exception)

# Clear existing mesh objects
bpy.ops.wm.read_factory_settings(use_empty=True)

def create_boundary(x0, y0, z0, x1, y1, z1):
    # Create a new mesh for the boundary
    bpy.ops.mesh.primitive_cube_add(size=1)
    boundary = bpy.context.object
    boundary.scale = [(x1 - x0) / 2, (y1 - y0) / 2, (z1 - z0) / 2]
    boundary.location = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]

def create_window(x, y, z, xdelta, ydelta, zdelta, qw, qx, qy, qz, xangdelta, yangdelta, zangdelta, texture_file):
    # Create a new mesh for the window
    bpy.ops.mesh.primitive_cube_add(size=1)
    window = bpy.context.object  # Get the active object
    if window:
        # Continue with material creation and assignment
        window.scale = [xdelta, ydelta, zdelta]
        window.location = [x, y, z]

        # Set the window orientation using the quaternion
        window.rotation_quaternion = [qw, qx, qy, qz]

        # Apply Euler angle variation
        bpy.context.active_object.rotation_euler = [xangdelta, yangdelta, zangdelta]

        # Add a texture to the window object
        if texture_file:
            # Create a new material
            try:
                window_material = bpy.data.materials.new(name="Window_Material")
            except Exception as e:
                print("Error creating material:", e)

            # Assign the material to the window object
            window.data.materials.append(window_material)
            print("Window materials:", window.data.materials)

            # Create an image texture node
            image_texture = window_material.node_tree.nodes.new('ShaderNodeTexImage')
            try:
                image_texture.image = bpy.data.images.load(texture_file)
            except Exception as e:
                print("Error loading texture:", e)

            # Connect the image texture to the material's surface
            shader_node = window_material.node_tree.nodes["Principled BSDF"]
            window_material.node_tree.links.new(shader_node.inputs["Base Color"], image_texture.outputs["Color"])
    
        else:
            print("No active object found.")

# Define the boundary and window data file
env_path = cfg['env']['main_path']
map_file = cfg['env']['map_file']
env_path = os.path.expanduser(os.path.join(env_path, map_file))

with open(env_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    tokens = line.strip().split()
    
    if tokens[0] == 'boundary':
        x0, y0, z0, x1, y1, z1 = map(float, tokens[1:])
        create_boundary(x0, y0, z0, x1, y1, z1)
    
    elif tokens[0] == 'window':
        x, y, z, xdelta, ydelta, zdelta, qw, qx, qy, qz, xangdelta, yangdelta, zangdelta = map(float, tokens[1:])
        texture_path = cfg['textures']['main_path']
        text_file_name = cfg['textures']['pic']
        text_file = os.path.expanduser(os.path.join(texture_path, text_file_name))
        print("Texture file path:", text_file)
        create_window(x, y, z, xdelta, ydelta, zdelta, qw, qx, qy, qz, xangdelta, yangdelta, zangdelta, text_file)

stored_path = cfg['blender_location']['main_path']
st_file_name = cfg['blender_location']['file_name']
blend_file = os.path.expanduser(os.path.join(stored_path, st_file_name))

bpy.ops.wm.save_as_mainfile(filepath = blend_file)
