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

# def send_batch():
#     files = []
#     for filename in os.listdir(IMAGE_FOLDER):
#         path = os.path.join(IMAGE_FOLDER, filename)
#         files.append(("files", (filename, open(path, "rb"), "image/jpeg")))
        
#     print("Number of files:", len(files))
    
#     start_time = time.time()
#     response = requests.post(API_URL, files=files)
#     end_time = time.time()
    
#     elapsed_time = end_time - start_time
#     print(f"Elapsed time for batch request: {elapsed_time:.2f} seconds")
#     print(response.json())
    
#     return response.json()

def send_batch():
    files = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(IMAGE_FOLDER, filename)
            files.append(("files", (filename, open(path, "rb"), "image/jpeg")))
    print("Number of files:", len(files))
    
    response = requests.post(API_URL, files=files)
    try:
        json_response = response.json()
    except Exception as e:
        print("Error decoding JSON:", e)
        json_response = {}
    
    return json_response

def main():
    total_batches = 10
    batch_results = []
    
    overall_start = time.time()
    
    for i in range(total_batches):
        print(f"\nSending batch {i+1} of {total_batches}")
        batch_response = send_batch()
        cumulative_elapsed = time.time() - overall_start
        batch_results.append((batch_response, cumulative_elapsed))
        print(f"Batch {i+1} completed at cumulative time: {cumulative_elapsed:.2f} seconds")
    
    print("\nAll batches completed. Summary:")
    for idx, (res, t) in enumerate(batch_results, start=1):
        print(f"Batch {idx}: Cumulative time from start = {t:.2f} seconds, Response = {res}")

if __name__ == "__main__":
    main()