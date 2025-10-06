# Image Processor

A sample FastAPI application that demonstrates asynchronous image processing using Celery and Redis.

## Features

- Upload images (JPG, JPEG, PNG, WebP, GIF)
- Asynchronous image processing with Celery
- Image resizing (500x500)
- Text watermarking
- Redis as message broker

## Tech Stack

- **FastAPI** - Web framework
- **Celery** - Task queue
- **Redis** - Message broker
- **Pillow** - Image processing
- **Docker** - Containerization

## Quick Start

1. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## API Endpoints

- `POST /upload-image` - Upload an image for processing
- `GET /task-status/{task_id}` - Check processing status
- `GET /ping` - Health check

## Usage Example

1. Upload an image:
   ```bash
   curl -X POST "http://localhost:8000/upload-image" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your-image.jpg"
   ```

2. Check processing status:
   ```bash
   curl "http://localhost:8000/task-status/{task_id}"
   ```

3. Access processed image:
   ```
   http://localhost:8000/static/watermarked_{filename}.png
   ```

