import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import List
import shutil

# model inference function
from server.models.segmentation import process_image

app = FastAPI()

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    
    try:
        # temp directory
        temp_dir = "/tmp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # model inference
        result = process_image(temp_path)
        
        
        os.remove(temp_path)
        
        # Return the result as JSON
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/upload-image-batch")
async def upload_images(files: List[UploadFile] = File(...)):

    results = []
    temp_dir = "/tmp"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        for file in files:
            temp_path = os.path.join(temp_dir, file.filename)
            
            
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            
            result = process_image(temp_path)
            results.append({"filename": file.filename, "result": result})
            
            
            os.remove(temp_path)
        
        return JSONResponse(content={"results": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# # Here starts the Celery + Redis approach
# # Self Note: to run, "celery -A server.queue.task_queue.celery_app worker --loglevel=info"
# #           Then regular FastAPI server like regular "uvicorn server.api.routes:app --reload"

# Run this to increase the number of workers, for now it is 4
# celery -A server.queue.task_queue.celery_app worker --loglevel=info --concurrency=4
from server.queue.task_queue import process_image_task

@app.post("/upload-image-celery")
async def upload_images_celery(files: List[UploadFile] = File(...)):

    task_ids = []
    temp_dir = "/tmp"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        for file in files:
            unique_filename = f"{uuid.uuid4()}_{file.filename}"
            temp_path = os.path.join(temp_dir, unique_filename)
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            
            task = process_image_task.delay(temp_path)
            task_ids.append({"filename": unique_filename, "task_id": task.id})
            
        
        return JSONResponse(content={"tasks": task_ids})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/upload-image-celery")
# async def upload_image_celery(file: UploadFile = File(...)):
#     try:
#         temp_dir = "/tmp"
#         os.makedirs(temp_dir, exist_ok=True)
#         temp_path = os.path.join(temp_dir, file.filename)
        
#         with open(temp_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
        
#         # call the Celery task
#         task = process_image_task.delay(temp_path)
        
#         return JSONResponse(content={"task_id": task.id})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    # to check status of the task
    task = process_image_task.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": task.state, "result": None}
    elif task.state != "FAILURE":
        return {"status": task.state, "result": task.result}
    else:
        return {"status": task.state, "result": str(task.info)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
