from asyncio import gather, to_thread
from fastapi import APIRouter, UploadFile, Depends, Form

from tasks.handle_document import handle_document

from utils.file_type_checker import get_ext_and_mime
from utils.authorization import is_client
from database.models import Key
from database.db import get_session

from routes.chunk import ChunkRequest, chunk
from typing import Optional

router = APIRouter()

@router.post("/upload")
async def upload_files(files: list[UploadFile], key: Key = Depends(is_client)):

    # You can do the usage tracking
    # Return the usage along the text
    # Get all the usages here
    # Update the db (with get_session() as session:)

    async def handle_file(file: UploadFile):
        # Read file content as bytes
        file_content = await file.read()  # This is bytes
        
        # Get the file type and MIME type
        file_type, file_mime = get_ext_and_mime(file, file_content)
        print(f"Identified file type: {file_type} with MIME type {file_mime}")
        
        # Pass file content (bytes), file type, and MIME type to Celery task
        task = handle_document.delay(file_content, file_type, file_mime)
        return task.get()

    # Step 1: Extract text from files using Celery and await results
    file_tasks = [handle_file(file) for file in files]
    extracted_texts = await gather(*file_tasks)
    return extracted_texts

    # FIXME:

    # if chunking is None: return extracted_texts
    
    # # Step 2: Chunk the extracted text based on the chunker_type and chunk_size
    # # Note: yeah i've modified this part to use the chunk function from the chunk.py file
    # chunk_tasks = [chunk(ChunkRequest(**chunking.model_dump(exclude="text"), text=text)) for text in extracted_texts]
    # chunked_results = await gather(*chunk_tasks)
    # return chunked_results
