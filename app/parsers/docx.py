from parsers.parser import Parser
from parsers.pdf import PdfParser
import io
import docx2txt
from magika import Magika
from zipfile import ZipFile
import mammoth
import pdfkit
from asyncio import run



class DocxParser(Parser):
    def parse(self, mime_type: str) -> str:
        # Check for images in the DOCX file
        images_present = self.extract_images_from_docx(self.data)
        
        if images_present:
            # Convert DOCX to PDF in memory
            pdf_data = self.convert_docx_to_pdf_in_memory(self.data)
            
            # Use PdfParser to process the PDF data
            pdf_parser = PdfParser(data=pdf_data)
            full_text = run(pdf_parser.aparse(mime_type='application/pdf'))
        else:
            # Extract text directly from the DOCX file
            full_text = self.extract_text_from_docx(self.data)
        
        return full_text
    
    @staticmethod
    def extract_images_from_docx(file_content):
        """
        Extract images from the .docx file in-memory without saving to disk,
        using Magika to identify images.
        """
        images = []
        magika = Magika()
        with io.BytesIO(file_content) as doc_stream:
            with ZipFile(doc_stream, 'r') as docx_zip:
                for file_name in docx_zip.namelist():
                    with docx_zip.open(file_name) as file:
                        file_bytes = file.read()
                        file_mk = magika.identify_bytes(file_bytes).output
                        file_type = file_mk.ct_label
                        file_mime = file_mk.mime_type
                        # Check if the file is an image
                        if 'png' in file_type or 'jpeg' in file_type:
                            print(f"Identified file {file_name} as type {file_type} with MIME type {file_mime}")
                            images.append((file_bytes, file_name, file_mime))
        if len(images) == 0:
            return False
        return True

    def convert_docx_to_pdf_in_memory(self, docx_bytes):
        # Step 1: Convert DOCX to HTML using Mammoth (in-memory)
        with io.BytesIO(docx_bytes) as docx_io:
            result = mammoth.convert_to_html(docx_io)

        # Step 2: Convert HTML to PDF in-memory using pdfkit
        pdf_bytes = pdfkit.from_string(result.value, False)  # False tells pdfkit to return bytes instead of writing to a file

        return pdf_bytes


    def extract_text_from_docx(self, docx_bytes):
        # Use python-docx to extract text from the DOCX file
        full_text = docx2txt.process(io.BytesIO(docx_bytes))
        return full_text

    def __del__(self):
        pass
