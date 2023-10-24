import bpy
import math

# Set the output directory
output_directory = "/home/ankush/Desktop/abhardwaj_p3a/output_images"


# Set the number of photos and angles
num_photos = 36  # Change the number of photos as needed
angle_increment = 360.0 / num_photos

# Set the camera parameters
camera_distance = 5.0  # Distance from the object
camera_height = 2.0  # Height of the camera above the object

# Set the output format and output file type
output_format = 'PNG'  # Change the image format if needed

# Set the output resolution (optional)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Loop through different angles and render images
for i in range(num_photos):
    angle = math.radians(i * angle_increment)
    camera = bpy.data.objects["Camera"]  # Assuming your camera is named "Camera"
    camera.location.x = camera_distance * math.cos(angle)
    camera.location.y = camera_distance * math.sin(angle)
    camera.location.z = camera_height
    camera.rotation_euler = (0, 0, angle)

    # Set the output file path based on the angle
    output_file = f"{output_directory}photo_{i:03d}.{output_format.lower()}"

    # Render the image
    bpy.ops.render.render(write_still=True)

# Delete the camera (optional)
bpy.ops.object.select_all(action='DESELECT')
camera.select_set(True)
bpy.ops.object.delete()

