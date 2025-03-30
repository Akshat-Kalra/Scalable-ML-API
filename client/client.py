# simple client to test the server

import time
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
        
    print("Number of files:", len(files))
    
    start_time = time.time()
    response = requests.post(API_URL, files=files)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"Elapsed time for batch request: {elapsed_time:.2f} seconds")
    print(response.json())
    
    return response.json()

if __name__ == "__main__":
    send_batch()