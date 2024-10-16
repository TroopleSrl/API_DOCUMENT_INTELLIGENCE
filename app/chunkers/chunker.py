class Chunker:

    def __init__(self, text: str):
        self.text = text

    def chunk(self):
        raise NotImplementedError("Subclasses must implement this method")

