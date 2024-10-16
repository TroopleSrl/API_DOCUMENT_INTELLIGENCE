from fastapi import APIRouter, UploadFile, Form
from tasks.apply_chunking import chunk_text
from magika import Magika
import asyncio
from tasks.handle_document import handle_document

router = APIRouter()

@router.post("/upload")
async def upload_files(files: list[UploadFile], chunker_type: str = Form(...), chunk_size: int = Form(...)):
    magika = Magika()
    extracted_texts = []
    
    # Step 1: Handle file uploads asynchronously and extract text
    async def handle_file(file):
        file_content = await file.read()
        file_mk = magika.identify_bytes(file_content).output
        file_type = file_mk.ct_label
        file_mime = file_mk.mime_type
        print(f"Identified file type: {file_type} with MIME type {file_mime}")
        task = handle_document.delay(file_content, file_type, file_mime)
        return task.get()  # Blocking call to get result from Celery task
    
    tasks = [handle_file(file) for file in files]
    extracted_texts = await asyncio.gather(*tasks)
    
    # Step 2: Chunk the extracted text based on the chunker_type and chunk_size
    async def chunk_text_async(text):
        task = chunk_text.delay(text, chunker_type, chunk_size)
        return task.get()  # Blocking call to get result from Celery task
    
    chunk_tasks = [chunk_text_async(text) for text in extracted_texts]
    chunked_results = await asyncio.gather(*chunk_tasks)
    
    # Step 3: Return the chunked text results
    return chunked_results
