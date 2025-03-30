FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir click>=8.0.0

    
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
