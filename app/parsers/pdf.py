from parsers.parser import Parser
from connectors.google import GeminiLLM
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from asyncio import gather, run
from settings import get_settings

class PdfParser(Parser):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gemini = GeminiLLM()

    def parse(self, mime_type: str) -> str:
        # Ensure we're returning a serializable result
        return run(self.aparse(mime_type))

    async def aparse(self, mime_type: str = "application/pdf") -> str:
        text = ""
        if mime_type.lower() == "application/pdf":
            self.pdf = PdfReader(BytesIO(self.data))
            self.splits = self.split_pdf_group_of_pages(2)
            print(f"Split into {len(self.splits)} groups of pages")
            
            # Ensure we upload files and get the texts in an async way, but only return the text
            uploads = await gather(*[self.gemini.upload_file(split, mime_type, wait=False) for split in self.splits])
            files = await gather(*[self.gemini.wait_for_file(file) for file in uploads])
            texts = await gather(*[self.gemini.chat(get_settings().USER_PROMPT, files=[file]) for file in files])
            text = " ".join(texts)
        else:
            await self.gemini.upload_file(BytesIO(self.data), mime_type, wait=True)
            text = await self.gemini.chat(get_settings().USER_PROMPT)

        # Ensure only the final result (a string) is returned
        del self.gemini
        return text

    def split_pdf_group_of_pages(self, pages_per_group: int = 2) -> list[BytesIO]:
        splits = []
        for i in range(0, len(self.pdf.pages), pages_per_group):
            writer = PdfWriter()
            bio = BytesIO()
            idx_start = i
            idx_end = min(i + pages_per_group, len(self.pdf.pages))
            for page in self.pdf.pages[idx_start:idx_end]:
                writer.add_page(page)
            writer.write(bio)
            bio.seek(0)  # Reset buffer position for reading
            splits.append(bio)
        return splits
