from fastapi import APIRouter, UploadFile
from typing import List
from app.functions.parser import extract_text_from_file
from app.connectors.gemini import handle_with_gemini

router = APIRouter()


@router.post("/uploadfiles/")
async def upload_files(files: List[UploadFile]):
    results = {}

    for file in files:
        try:
            filename = file.filename
            print(f"Processing file: {filename}")

            # Read the file content into memory
            file_content = await file.read()

            # Determine file handling based on file content
            text_result = extract_text_from_file(file_content, filename)
            if text_result != "Unsupported format for local extraction.":
                # Processed with local extraction logic
                results[filename] = text_result
            else:
                # Use Celery to process with Gemini API
                task = handle_with_gemini.delay(file_content, filename)
                results[filename] = {"task_id": task.id}
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
            results[filename] = f"Error: {str(e)}"

    return results

@router.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    from app.celery_app import celery_app
    task_result = celery_app.AsyncResult(task_id)
    if task_result.state == 'PENDING':
        response = {'state': task_result.state, 'status': 'Pending...'}
    elif task_result.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'result': task_result.result
        }
    else:
        response = {
            'state': task_result.state,
            'status': str(task_result.info),
        }
    return response
