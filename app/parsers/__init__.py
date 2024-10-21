from .parser import Parser
from .docx import DocxParser
from .pdf import PdfParser

def get_parser(type: str) -> type[Parser]:
    match type:
        case "docx":
            return DocxParser
        case "pdf" | "png" | "jpeg":
            return PdfParser
        case _:
            raise ValueError(f"Unsupported document type: {type}")