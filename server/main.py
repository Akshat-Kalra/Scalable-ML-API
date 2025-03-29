from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List
import os
from datetime import datetime

app = FastAPI(title="Food Segmentation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """
    Process a single image to detect and segment food items.
    Returns the area of each detected food item.
    """
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # TODO: Add image processing logic here
        # 1. Load image using OpenCV
        # 2. Run YOLOv8 inference
        # 3. Perform segmentation
        # 4. Calculate areas
        
        return {
            "status": "success",
            "message": "Image processed successfully",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-batch")
async def process_batch(files: List[UploadFile] = File(...)):
    """
    Process multiple images in batch.
    Returns the area of each detected food item for each image.
    """
    try:
        results = []
        for file in files:
            # Process each file
            result = await process_image(file)
            results.append(result)
        
        return {
            "status": "success",
            "message": f"Processed {len(files)} images",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
