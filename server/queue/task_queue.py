import os
from celery import Celery
from server.models.segmentation import process_image

# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# I'm using Celery + Redis approach, I talked about its benefits in the first interview aswell :)
celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

@celery_app.task
def process_image_task(image_path: str):
    result = process_image(image_path)
    
    
    if os.path.exists(image_path):
        os.remove(image_path)
    return result