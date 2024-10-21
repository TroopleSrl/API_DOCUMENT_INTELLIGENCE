from pydantic import BaseModel
from typing import Optional

class ChunkRequest(BaseModel):
    text: str = ""
    chunker_type: str = "fixed" 
    chunk_size: int = 500