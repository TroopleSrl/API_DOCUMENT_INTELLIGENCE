from worker import celery_app as app
from parsers import get_parser

@app.task(name="handle_document")
def handle_document(document: bytes, type: str, mime: str):
    try:
        print(f"Handling document of type {type} with MIME type {mime}")
        parser = get_parser(type)(document)
        text = parser.parse(mime)
        del parser
        return text
    except Exception as e:
        print(f"Failed to handle document of type {type} with MIME type {mime}")
        print(e)
