class Parser:

    def __init__(self, data: bytes):
        self.data = data

    def parse(self, mime_type: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")