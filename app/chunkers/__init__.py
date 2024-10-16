from .chunker import Chunker
from .fixed_chunker import FixedSizeChunker

def get_chunker(chunker_type: str):
    match chunker_type:
        case "fixed":
            return FixedSizeChunker
        case _:
            raise ValueError(f"Unsupported chunker type: {chunker_type}")