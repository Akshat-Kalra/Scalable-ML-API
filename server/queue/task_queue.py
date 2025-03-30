import os
from celery import Celery
from server.models.segmentation import process_image

# I'm using Celery + Redis approach, I talked about its benefits in the first interview aswell :)
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_image_task(image_path: str):
    result = process_image(image_path)
    
    
    if os.path.exists(image_path):
        os.remove(image_path)
    return result