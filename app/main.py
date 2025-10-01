from fastapi import FastAPI, UploadFile, File, HTTPException
from tasks import long_running_task

app = FastAPI() 

@app.get("/ping")
async def read_root():
    return {"message": "API running successfully"}

ALLOWED_IMAGE_TYPES = {
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

# @app.post("/upload-image")
# async def upload_image(file: UploadFile = File(...)):
#     if file.content_type not in ALLOWED_IMAGE_TYPES:
#         raise HTTPException(
#             status_code=400,
#             detail="Attached file is not an image."
#         )
#     return {"filename": file.filename}

@app.post("/add-task/")
def add_task(x: int, y: int):
    task = long_running_task.delay(x, y)  # send task to Redis
    return {"task_id": task.id}           # return task ID

@app.get("/task-status/{task_id}")
def get_status(task_id: str):
    from celery_app import celery
    result = celery.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }