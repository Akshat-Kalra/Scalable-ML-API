# client that sends multiple batches concurrently

import time
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "http://localhost:8000/upload-image-celery"

IMAGE_FOLDER = "test_images"

def send_batch():
    
    files = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(IMAGE_FOLDER, filename)
            files.append(("files", (filename, open(path, "rb"), "image/jpeg")))
    print("Number of files:", len(files))
    response = requests.post(API_URL, files=files)
    return response.json()

def poll_task(task_id, interval=1):
    """
    Polls the status endpoint in the server for the given task_id until its status is SUCCESS or FAILURE.
    Returns the final task result.
    """
    status_url = f'http://localhost:8000/task-status/{task_id}'
    while True:
        response = requests.get(status_url)
        data = response.json()
        print(f"Polling task {task_id}: {data['status']}")
        if data["status"] in ["SUCCESS", "FAILURE"]:
            return data
        time.sleep(interval)

def send_and_poll():
    
    start_time = time.time()
    
    
    batch_response = send_batch()
    print("Batch response:", batch_response)
    
    tasks = batch_response.get("tasks", [])
    if not tasks:
        print("No tasks received")
        return None
    
    
    last_task_id = tasks[-1]["task_id"]
    print(f"Polling for last task id: {last_task_id}")
    
    final_result = poll_task(last_task_id)
    
    elapsed_time = time.time() - start_time
    return elapsed_time, final_result

def main():
    result_list = []
    
    concurrent_batches = 10
    
    with ThreadPoolExecutor(max_workers=concurrent_batches) as executor:
        futures = [executor.submit(send_and_poll) for _ in range(concurrent_batches)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                elapsed_time, poll_result = result
                result_list.append(elapsed_time)
                print(f"Batch completed in {elapsed_time:.2f}")
            else:
                print("No tasks received.")
                
    print("All batches completed")
    print("Results:")
    for i, result in enumerate(result_list, start=1):
        print(f"Batch {i}")
        print(result)
    
if __name__ == "__main__":
    main()
