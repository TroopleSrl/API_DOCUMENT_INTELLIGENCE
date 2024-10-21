from fastapi import APIRouter, UploadFile, Form
from tasks.apply_chunking import chunk_text
from file_type_checker.file_type_checker import get_ext_and_mime
from tasks.handle_document import handle_document
import asyncio

router = APIRouter()

@router.post("/upload")
async def upload_files(files: list[UploadFile], chunker_type: str = Form(...), chunk_size: int = Form(...)):

    async def handle_file(file: UploadFile):
        # Read file content as bytes
        file_content = await file.read()  # This is bytes
        
        # Get the file type and MIME type
        file_type, file_mime = get_ext_and_mime(file, file_content)
        print(f"Identified file type: {file_type} with MIME type {file_mime}")
        
        # Pass file content (bytes), file type, and MIME type to Celery task
        task = handle_document.delay(file_content, file_type, file_mime)
        
        # Offload task.get() to a separate thread to avoid blocking
        result = await asyncio.to_thread(task.get)
        return result

    # Step 1: Extract text from files using Celery and await results
    file_tasks = [handle_file(file) for file in files]
    extracted_texts = await asyncio.gather(*file_tasks)

    # Async function to chunk the extracted text
    async def chunk_text_async(text: str):
        # Send the chunking task to Celery
        task = chunk_text.delay(text, chunker_type, chunk_size)
        
        # Offload task.get() to a separate thread to avoid blocking
        result = await asyncio.to_thread(task.get)
        return result

    # Step 2: Chunk the extracted text based on the chunker_type and chunk_size
    chunk_tasks = [chunk_text_async(text) for text in extracted_texts]
    chunked_results = await asyncio.gather(*chunk_tasks)

    # Step 3: Return the chunked text results
    return {"chunked_results": chunked_results}
