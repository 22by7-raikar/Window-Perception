import os
import json
from PIL import Image, ImageDraw

# Load the JSON file with image and vertex coordinates
json_file_path = "/home/anuj/Desktop/AerialRobotics/apairaikar_p3a/Dataset/Train/image_vertex_mapping.json"  # Replace with the path to your JSON file
output_folder = "/home/anuj/Desktop/AerialRobotics/apairaikar_p3a/Dataset/Train/marked_images"  # Replace with the path to the output folder

with open(json_file_path, 'r') as json_file:
    image_vertex_mapping = json.load(json_file)

# Function to add yellow dots to the image
def add_dots_to_image(image_path, vertex_coordinates):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    for vertex_data in vertex_coordinates:
        x, y = vertex_data['image_coordinates']
        draw.ellipse([(x - 5, y - 5), (x + 5, y + 5)], fill="yellow")

    return img

# Process each image and add yellow dots
for image_path, vertex_coordinates in image_vertex_mapping.items():
    output_image = add_dots_to_image(image_path, vertex_coordinates)

    # Save the modified image to the output folder
    image_filename = os.path.basename(image_path)
    output_image_path = os.path.join(output_folder, image_filename)
    output_image.save(output_image_path)

    print(f"Processed image: {output_image_path}")

print("All images processed and saved to the output folder.")
