from parsers.parser import Parser
from connectors.google import GeminiLLM
from io import BytesIO

class PdfParser(Parser):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gemini = GeminiLLM()

    def parse(self, mime_type: str = "application/pdf") -> str:
        self.gemini.upload_file(BytesIO(self.data), mime_type, wait=True)
        chat = self.gemini.chat("Extract everything from the PDF file.")
        return chat

    def __del__(self):
        for _ in range(len(self.gemini.files)):
            self.gemini.remove_file(self.gemini.files[0])