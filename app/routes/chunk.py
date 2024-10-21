from fastapi import APIRouter
from pydantic import BaseModel
from tasks.apply_chunking import chunk_text 

router = APIRouter()

class ChunkRequest(BaseModel):
    text: str
    chunker_type: str
    chunk_size: int

@router.post("/chunk")
def chunk(chunk_request: ChunkRequest):
    # Call the synchronous Celery task
    task = chunk_text.delay(chunk_request.text, chunk_request.chunker_type, chunk_request.chunk_size)

    result = task.get()

    return {"result": result}
