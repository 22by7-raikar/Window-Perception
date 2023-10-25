# import json

# # Load your JSON data
# json_path = '/home/anuj/Desktop/AerialRobotics/apairaikar_p3a/Dataset/Train/image_vertex_mapping.json'
# with open(json_path, 'r') as json_file:
#     data = json.load(json_file)

# # Define the image dimensions (width and height)
# image_width = 300  # Replace with your image width
# image_height = 200  # Replace with your image height

# for image_path, keypoints in data.items():
#     label_path = f'/home/anuj/Desktop/AerialRobotics/apairaikar_p3a/Dataset/Train/labels/{image_path.split("/")[-1].replace(".png", ".txt")}'

#     with open(label_path, 'w') as label_file:
#         for keypoint in keypoints:
#             x, y = keypoint['image_coordinates']
#             x_normalized = x / image_width
#             y_normalized = y / image_height

#             # Map your keypoints to class indices based on your data.yaml
#             if keypoint['vertex_index'] == 0:
#                 class_index = 0
#             elif keypoint['vertex_index'] == 1:
#                 class_index = 1
#             elif keypoint['vertex_index'] == 2:
#                 class_index = 2
#             elif keypoint['vertex_index'] == 3:
#                 class_index = 3
#             else:
#                 class_index = 0  # Replace with the appropriate class index

#             label_file.write(f'{class_index} {x_normalized} {y_normalized} 0\n')


import json

# Load your JSON data
json_path = '/home/anuj/Desktop/AerialRobotics/apairaikar_p3a/Dataset/Train/image_vertex_mapping.json'
with open(json_path, 'r') as json_file:
    data = json.load(json_file)

# Define the image dimensions (width and height)
image_width = 300  # Replace with your image width
image_height = 200  # Replace with your image height

# Define a mapping of keypoints to class indices based on your data.yaml
keypoint_to_class_mapping = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

for image_path, keypoints in data.items():
    label_path = image_path.replace('/Train/Images/', '/Train/labels/').replace('.png', '.txt')

    with open(label_path, 'w') as label_file:
        for keypoint in keypoints:
            ax, ay = keypoint['image_coordinates']
            x_normalized = ax / image_width
            y_normalized = ay / image_height

            # Map your keypoints to class indices using the mapping
            class_index = keypoint_to_class_mapping.get(keypoint['vertex_index'], 0)

            label_file.write(f'{class_index} {x_normalized} {y_normalized} 0\n')
