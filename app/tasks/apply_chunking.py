from worker import celery_app as app
from chunkers import get_chunker

@app.task(name="chunk_text")
def chunk_text(text: str, chunker_type: str, chunk_size: int):
    try:
        ChunkerClass = get_chunker(chunker_type)
        chunker = ChunkerClass(chunk_size)
        chunks = list(chunker.chunk(text))

        del chunker
        return chunks
    except Exception as e:
        print("Failed to chunk the text")
        print(e)

