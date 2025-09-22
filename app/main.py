from fastapi import FastAPI, UploadFile, File, HTTPException

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

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Attached file is not an image."
        )
    return {"filename": file.filename}