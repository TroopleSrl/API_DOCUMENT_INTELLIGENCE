from fastapi import APIRouter
from pydantic import BaseModel
from tasks.apply_chunking import chunk_text 

router = APIRouter()

class ChunkRequest(BaseModel):
    text: str
    chunker_type: str
    chunk_size: int

@router.post("/chunk")
async def chunk(chunk_request: ChunkRequest):
    tasks = []
    task = chunk_text.delay(chunk_request.text, chunk_request.chunker_type, chunk_request.chunk_size)

    tasks.append(task)

    # Wait for all results
    if not tasks: return []
    results = [task.get() for task in tasks]
    return results

