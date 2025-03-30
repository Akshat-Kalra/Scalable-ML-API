import time
import requests
import os

API_URL = "http://localhost:8000/upload-image-celery"
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
    
    # start_time = time.time()
    response = requests.post(API_URL, files=files)
    # end_time = time.time()
    
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time for batch request: {elapsed_time:.2f} seconds")
    print(response.json())
    
    return response.json()

def poll_task(task_id, interval=1):
    
    status_url = f"http://localhost:8000/task-status/{task_id}"
    while True:
        response = requests.get(status_url)
        data = response.json()
        print(f"Polling task {task_id}: {data['status']}")
        if data["status"] == "SUCCESS" or data["status"] == "FAILURE":
            return data
        time.sleep(interval)

def main():
    
    start_time = time.time()
    
    
    batch_response = send_batch()
    print("Batch response:", batch_response)
    
    tasks = batch_response.get("tasks", [])
    if not tasks:
        print("No tasks received")
        return
    
    # getting the last task id
    last_task = tasks[-1]
    last_task_id = last_task["task_id"]
    
    print(f"Polling for last task id: {last_task_id}")
    
    
    final_result = poll_task(last_task_id)
    
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Last task {last_task_id} completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     send_batch()