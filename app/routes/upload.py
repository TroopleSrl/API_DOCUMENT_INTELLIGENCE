from fastapi import APIRouter, UploadFile

from tasks.handle_document import handle_document
from magika import Magika

router = APIRouter()

@router.post("/upload")
async def upload_files(files: list[UploadFile]):
    
    magika = Magika()
    tasks = []
    for file in files:
        file_content = file.file.read()
        file_mk = magika.identify_bytes(file_content).output
        file_type = file_mk.ct_label
        file_mime = file_mk.mime_type
        print(f"Identified file type: {file_type} with MIME type {file_mime}")
        task = handle_document.delay(file_content, file_type, file_mime)
        tasks.append(task)
    
    # Wait for all results
    if not tasks: return []
    results = [task.get() for task in tasks]
    return results

