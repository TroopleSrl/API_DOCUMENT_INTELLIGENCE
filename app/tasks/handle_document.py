from worker import celery_app as app
from parsers import get_parser

@app.task(name="handle_document")
def handle_document(document: bytes, file_type: str, mime: str):
    try:
        print(f"Handling document of type {file_type} with MIME type {mime}")
        
        # Ensure we're passing the correct bytes data into the parser
        parser = get_parser(file_type)(document)  # `document` should remain as `bytes`
        text = parser.parse(mime)
        print(f"Extracted text: {text}")
        # Clean up
        del parser
        return text
    
    except Exception as e:
        print(f"Failed to handle document of type {file_type} with MIME type {mime}")
        print(e)
        return None
