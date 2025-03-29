'''
Note: This script was run on Google Colab

And is used to download the Food-101 dataset and select 100 random images for testing the model.

No need to run this script, it is just for showing how I selected the images for testing the application.

The images are in test_images folder

'''


import os
import glob
import random
import shutil
import kagglehub
import zipfile
import shutil
from google.colab import files

# Download the Food-101 dataset
dataset_zip_path = kagglehub.dataset_download("dansbecker/food-101")
print("Dataset downloaded to:", dataset_zip_path)


if os.path.isdir(dataset_zip_path):
    extraction_dir = dataset_zip_path
    print("Dataset is already extracted in:", extraction_dir)
else:
    extraction_dir = dataset_zip_path[:-4] if dataset_zip_path.endswith('.zip') else dataset_zip_path
    os.makedirs(extraction_dir, exist_ok=True)
    with zipfile.ZipFile(dataset_zip_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)
    print("Dataset extracted to:", extraction_dir)

all_images = glob.glob(os.path.join(extraction_dir, "**", "*.jpg"), recursive=True)
print(f"Found {len(all_images)} images in the dataset.")

# Randomly select 100 images
num_images_to_select = 100
selected_images = random.sample(all_images, min(num_images_to_select, len(all_images)))
print(f"Selected {len(selected_images)} images for testing.")

# Define destination folder for client test images
destination_folder = "client/test_images"
os.makedirs(destination_folder, exist_ok=True)

# Copy the selected images to the destination folder
for image_file in selected_images:
    shutil.copy(image_file, destination_folder)
print(f"Copied {len(selected_images)} images to {destination_folder}")


folder_to_download = "client/test_images"
zip_filename = "test_images.zip"

shutil.make_archive("test_images", 'zip', folder_to_download)

files.download(zip_filename)


