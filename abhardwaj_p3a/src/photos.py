import bpy
import math

def position_camera(cam, angle_x, angle_y, x,y, focus_target):
    # Position the camera
    cam.location = (x, y, 0)
    
    # Clear existing track_to constraints from the camera
    for constraint in cam.constraints:
        if constraint.type == 'TRACK_TO':
            cam.constraints.remove(constraint)

    # Add track_to constraint to point the camera at the focus_target
    track_to = cam.constraints.new(type='TRACK_TO')
    track_to.target = focus_target
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'
    
    # Rotate the camera around the Z-axis
    cam.rotation_euler[2] = math.radians(angle_x)
    
    # Rotate the camera up or down around its local X-axis
    cam.rotation_euler[0] = math.radians(angle_y)

# Ensure you're in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Get the focus target and camera
focus_target = bpy.data.objects['Plane.001']
cam = bpy.data.objects['NN_cam']

# Parameters for camera positioning
angles_x = [0, 90, 180, 270]  # Around the object in the XZ plane
angles_y = [0, 30, 60, -30, -60]  # Above and below the object
radiusy = [0,0.5,1,1.5]  # Distance from the focus_target
radiusx = [0,0.5,1,1.5]
# Position camera at different angles and render images
render_path = "/home/ankush/Desktop/abhardwaj_p3a/output_images1/"  # Modify this path as needed
for y in radiusy:
    for x in radiusx:
        position_camera(cam, 0, 0, x,y, focus_target)
        bpy.context.scene.camera = cam
        bpy.context.scene.render.filepath = f"{render_path}render{x}_{y}.png"
        bpy.ops.render.render(write_still=True)

