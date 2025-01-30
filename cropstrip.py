from PIL import Image
import os

def crop_bottom_strip(image_path, output_path, strip_height):
    """
    Crops the bottom strip of an image.

    :param image_path: Path to the input image.
    :param output_path: Path to save the cropped image.
    :param strip_height: Height of the bottom strip to remove.
    """
    with Image.open(image_path) as img:
        width, height = img.size
        # Define the coordinates of the top left and bottom right corners of the new image
        crop_box = (0, 0, width, height - strip_height)
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)

# Example usage
folder_path = r'E:\NYX_GCP\winter_alamy_images'
output_folder = r'E:\NYX_GCP\crop'
strip_height = 20 
count = 0

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)
        crop_bottom_strip(image_path, output_path, strip_height)
        count += 1
        print(f"{count} Cropped image saved to {output_path}")
