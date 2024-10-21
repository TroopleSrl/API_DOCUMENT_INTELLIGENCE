from worker import celery_app as app
from chunkers import get_chunker

@app.task(name="chunk_text")
def chunk_text(text: str, chunker_type: str, chunk_size: int):
    try:
        # Fetch the appropriate chunker class (ensure it does not return functions)
        ChunkerClass = get_chunker(chunker_type)
        
        # Initialize the chunker
        chunker = ChunkerClass(chunk_size)

        # Perform chunking operation
        chunks = chunker.chunk(text)
        print(f"Chunks of text: {chunks}")
        # Log and ensure chunks is serializable (should be a list or dict)
        print(f"Chunks: {chunks}")
        if isinstance(chunks, list):  # Ensure chunks is a list
            return chunks
        else:
            raise ValueError("Chunking result must be a serializable list")

    except Exception as e:
        print(f"Failed to chunk the text: {e}")
        return None
