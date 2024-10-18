from chunkers.chunker import Chunker
import semchunk
from transformers import AutoTokenizer

class SemanticFakeChunker(Chunker):
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def chunk(self, text: str):
        chunk_size = self.chunk_size
        chunker = None

        # Try different chunking strategies, with fallbacks
        try:
            chunker = semchunk.chunkerify(AutoTokenizer.from_pretrained('umarbutler/emubert'), chunk_size)
        except Exception:
            try:
                chunker = semchunk.chunkerify('gpt-4', chunk_size)
            except Exception:
                chunker = semchunk.chunkerify('cl100k_base', chunk_size)

        # Fallback to simple word-based chunking
        if chunker is None:
            chunker = semchunk.chunkerify(lambda text: len(text.split()), chunk_size)

        return chunker(text)
