from chunkers.chunker import Chunker

class FixedSizeChunker(Chunker):
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def chunk(self, text: str):
        """Chunk the text into fixed-size chunks."""
        for i in range(0, len(text), self.chunk_size):
            yield text[i:i + self.chunk_size]
