# Food Segmentation and Area Calculation

This project implements a scalable server-side application for detecting and segmenting food items in images, and calculating their areas.

## Features

- Food item detection and segmentation using YOLOv8
- Area calculation for each detected food item
- Support for both single and batch image processing
- Scalable architecture with Docker support
- RESTful API endpoints

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- CUDA-capable GPU (recommended for better performance)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Using Docker:
```bash
docker-compose up --build
```

4. Without Docker:
```bash
# Start the server
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

1. Single Image Processing:
```
POST /process-image
Content-Type: multipart/form-data
file: <image_file>
```

2. Batch Processing:
```
POST /process-batch
Content-Type: multipart/form-data
files: <image_file1>
files: <image_file2>
...
```

## Client Usage

The client can be used to test the server:

```python
from client.client import FoodSegmentationClient

# Initialize client
client = FoodSegmentationClient()

# Process single image
result = client.process_single_image("path/to/image.jpg")

# Process multiple images
results = client.process_batch(["image1.jpg", "image2.jpg"])
```

## Scalability Features

1. Docker containerization for easy deployment
2. Redis for task queue management
3. Batch processing support
4. Asynchronous request handling

## Project Structure

```
.
├── server/
│   ├── main.py              # FastAPI application
│   ├── processing/          # Image processing modules
│   └── api/                 # API endpoints
├── client/
│   └── client.py           # Client implementation
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Performance Considerations

- The server can handle multiple concurrent requests
- Images are processed asynchronously
- Results are cached in Redis for faster retrieval
- Batch processing is optimized for multiple images

## Future Improvements

1. Add authentication and rate limiting
2. Implement result caching
3. Add more food detection models
4. Improve error handling and logging
5. Add monitoring and metrics