# Zepp Health Intern Home Assignment Submission
# By Akshat Kalra

## Submission Report
https://economic-dash-19d.notion.site/zepp-health-assignment-report-akshat-ubc?pvs=4

## Setup Instructions

### 1. Clone the Repository

```bash
git clone `https://github.com/Akshat-Kalra/Zepp-Health-Assignment.git`
cd Zepp-Health-Assignment
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up redis
```bash
redis-server
```

### 5. Run the FastAPI Server
```bash
uvicorn server.api.routes:app --reload
```

### 6. Run the Celery Worker
```bash
celery -A server.queue.task_queue.celery_app worker --loglevel=info --concurrency=2
```
### Adjust the --concurrency parameter based on your system's resources.


### 7. API Endpoints
**Redis + Celery Endpoint:**

For batch processing, send a POST request to `http://localhost:8000/upload-images-celery` and poll task status at `http://localhost:8000/task-status/<task_id>`.

**Simple FastAPI Endpoint (Just for performance comparison):**

- For processing single image
`http://localhost:8000/upload-image`

- For batch processing
`http://localhost:8000/upload-image-batch`



### 8. Running the Client Script
There are 2 client scripts in teh `client/` folder.

`client/client_concurrent.py` is designed to send multiple batch requests concurrently. It sends 10 batches of 100 images each to the `/upload-image-celery` endpoint and then polls the task status of the last task in each batch. This allows you to measure the cumulative time taken for each batch from the moment the first batch is sent.

To run it
From another terminal session run:
```bash
cd client
python client_concurrent.py
```

`client/client.py` sends 10 batches of 100 images to the simple FastAPI endpoint `/upload-image-batch`. This is designed for just comparing performance with the ` /upload-image-celery`.

To run it
From another terminal session run:
```bash
cd client
python client.py
```