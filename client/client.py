import requests

API_URL = "http://localhost:8000/upload-image"
image_path = "Food.jpeg"

with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    response = requests.post(API_URL, files=files)
    print(response.json())