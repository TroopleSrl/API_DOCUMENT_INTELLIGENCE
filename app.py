from fastapi import FastAPI, UploadFile, File
from celery import Celery
from typing import List
from extract import extract_text_from_file
import shutil
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize Celery
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Celery task for extracting text asynchronously
@celery.task
def extract_text_task(file_paths):
    result = {}
    for file_path in file_paths:
        file_text = extract_text_from_file(file_path)
        result[file_path] = file_text
        os.remove(file_path)  # Clean up the file after processing
    return result

# API endpoint to accept multiple files
@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    file_paths = []

    # Save uploaded files to disk
    for file in files:
        file_path = f"temp_files/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)

    # Launch Celery task to process files
    task = extract_text_task.delay(file_paths)
    return {"task_id": task.id}

# API endpoint to check the task result
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = extract_text_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return {"status": "Processing..."}
    
    if task.state != 'FAILURE':
        return {"status": "Completed", "result": task.result}
    else:
        return {"status": "Failed", "error": str(task.info)}
