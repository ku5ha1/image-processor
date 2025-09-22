from fastapi import FastAPI, UploadFile, File   

app = FastAPI() 

@app.get("/ping")
async def read_root():
    return {"message": "API running successfully"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename}