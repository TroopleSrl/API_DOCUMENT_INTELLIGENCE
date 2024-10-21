from fastapi import APIRouter
from tasks.apply_chunking import chunk_text 

from models.chunk_request import ChunkRequest

router = APIRouter()


@router.post("/chunk")
def chunk(chunk_request: ChunkRequest):
    task = chunk_text.delay(chunk_request.text, chunk_request.chunker_type, chunk_request.chunk_size)
    result = task.get()
    return result

