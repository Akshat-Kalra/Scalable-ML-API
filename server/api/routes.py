from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
