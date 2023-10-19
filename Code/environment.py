import os
import yaml
from scipy import io
import bpy
import math

curr_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(curr_dir, 'configs/cfg.yaml')) as file:
    try:
        print(curr_dir)
        cfg = yaml.safe_load(file)

    except yaml.YAMLError as exception:
        print(exception)

# Clear existing mesh objects
bpy.ops.wm.read_factory_settings(use_empty=True)

def setup_window_material(texture_path):
    # Create a new material for the window
    window_material = bpy.data.materials.new(name="WindowMaterial")

    # Enable 'Use nodes' for the material
    window_material.use_nodes = True

    # Get the material node tree
    node_tree = window_material.node_tree

    # Clear default nodes
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Add a ShaderNodeTexImage node to load the texture

    # Load the texture for the window
    texture_location = cfg["textures"]["main_path"]
    texture_file = cfg["textures"]["pic"]
    texture_path = os.path.expanduser(os.path.join(texture_location, texture_file))

    # Create the window material with the texture
    window_material = setup_window_material(texture_path)

    texture_node = node_tree.nodes.new('ShaderNodeTexImage')
    texture_node.location = (0, 0)
    texture_node.image = bpy.data.images.load(texture_path)

    # Connect the texture node to the material output
    shader_output = node_tree.nodes["Material Output"]
    node_tree.links.new(texture_node.outputs["Color"], shader_output.inputs["Surface"])

    return window_material


def create_boundary(x0, y0, z0, x1, y1, z1):
    # Create a new mesh for the boundary
    bpy.ops.mesh.primitive_cube_add(size=1)
    boundary = bpy.context.object
    boundary.scale = [(x1 - x0) / 2, (y1 - y0) / 2, (z1 - z0) / 2]
    boundary.location = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]

def create_window(x, y, z, xdelta, ydelta, zdelta, qw, qx, qy, qz, xangdelta, yangdelta, zangdelta, texture_path):
    # Create a new mesh for the window
    bpy.ops.mesh.primitive_cube_add(size=1)
    window = bpy.context.object
    window.scale = [xdelta, ydelta, zdelta]
    window.location = [x, y, z]

    # Set the window orientation using the quaternion
    window.rotation_quaternion = [qw, qx, qy, qz]

    # Apply Euler angle variation
    bpy.context.active_object.rotation_euler = [xangdelta, yangdelta, zangdelta]

    # Add a texture to the window object
    if texture_path:
        # Create a new material
        window_material = bpy.data.materials.new(name="Window_Material")

        # Assign the material to the window object
        window.data.materials.append(window_material)

        # Create an image texture node
        image_texture = window_material.node_tree.nodes.new('ShaderNodeTexImage')
        image_texture.image = bpy.data.images.load(texture_path)

        # Connect the image texture to the material's surface
        shader_node = window_material.node_tree.nodes["Principled BSDF"]
        window_material.node_tree.links.new(shader_node.inputs["Base Color"], image_texture.outputs["Color"])

def create_block(xmin, ymin, zmin, xmax, ymax, zmax, r, g, b, robot_width, robot_length, robot_height):
    bloat_width = robot_width/2
    bloat_length = robot_length/2
    bloat_height = robot_height/2
    bpy.ops.mesh.primitive_cube_add(scale=((xmax-xmin)/2 + (bloat_width), (ymax-ymin)/2 + (bloat_length), (zmax-zmin)/2 + (bloat_height)))
    block = bpy.context.active_object
    block.location.x = (xmax+xmin) / 2
    block.location.y = (ymax+ymin) / 2
    block.location.z = (zmax+zmin) / 2
    material = bpy.data.materials.new(name="BlockMaterial")
    block.data.materials.append(material)
    material.diffuse_color = (r / 255, g / 255, b / 255, 1)


def create_sphere(location, r, g, b, radius = 0.01):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    sphere = bpy.context.active_object
    material = bpy.data.materials.new(name="SphereMaterial")
    sphere.data.materials.append(material)
    material.diffuse_color = (r / 255, g / 255, b / 255, 1)

def create_cylinder(p1, p2, radius=0.01):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    dist = ((dx)**2 + (dy)**2 + (dz)**2)**0.5
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=dist, location=(dx/2 + p1[0], dy/2 + p1[1], dz/2 + p1[2]))
    phi = math.atan2(dy, dx)
    theta = math.acos(dz/dist)
    bpy.context.active_object.rotation_euler[1] = theta
    bpy.context.active_object.rotation_euler[2] = phi


# def create_nodes_spheres(path_found):
#     for i in range(1, len(path)):
#         create_sphere(path[i], 0, 0, 255, radius=0.05)
#         create_cylinder(path[i], path[i -1])
        
        
def clear_scene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

