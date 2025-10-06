import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from .tasks import process_image
from celery.result import AsyncResult
from .celery_app import app as celery_app

app = FastAPI()

ALLOWED_IMAGE_TYPES = {
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

@app.get("/ping")
async def read_root():
    return {"message": "API running successfully"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Attached file is not an image."
        )
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    upload_path = os.path.join(upload_dir, file.filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())

    task = process_image.delay(upload_path)

    return {"task_id": task.id, "filename": file.filename}

@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    if task.status == "PENDING":
        return {"task_id": task_id, "status": task.status, "processed_image_url": None}

    elif task.status == "SUCCESS":
        processed_path = task.result 
        processed_url = f"/static/{os.path.basename(processed_path)}"

        return {
            "task_id": task_id,
            "status": task.status,
            "processed_image_url": processed_url
        }
    elif task.status == "FAILURE":
        return {
            "task_id": task_id,
            "status": task.status,
            "error": str(task.result)
        }
    else:
        return {"task_id": task_id, "status": task.status, "processed_image_url": None}
