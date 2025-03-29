import requests
import os

API_URL = "http://localhost:8000/upload-image-batch"
# image_path = "Food.jpeg"
IMAGE_FOLDER = "test_images"

# with open(image_path, "rb") as image_file:
#     files = {"file": image_file}
#     response = requests.post(API_URL, files=files)
#     print(response.json())

def send_batch():
    files = []
    for filename in os.listdir(IMAGE_FOLDER):
        path = os.path.join(IMAGE_FOLDER, filename)
        files.append(("files", (filename, open(path, "rb"), "image/jpeg")))
    print(len(files))
    response = requests.post(API_URL, files=files)
    print(response.json())

if __name__ == "__main__":
    send_batch()