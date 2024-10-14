from parsers.parser import Parser
from docx import Document
from io import BytesIO

class DocxParser(Parser):
    
    def parse(self, mime_type: str) -> str:
        doc = Document(BytesIO(self.data))
        return '\n'.join([para.text for para in doc.paragraphs])
    
    def __del__(self):
        pass