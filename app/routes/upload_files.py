from fastapi import APIRouter, UploadFile
from typing import List
from app.functions.parser import extract_text_from_file
from app.connectors.gemini import handle_with_gemini

# Create a router instance
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

            # Determine file handling based on file extension
            if filename.lower().endswith(('.docx', '.xlsx', '.eml')):
                # Process file with local extraction logic
                results[filename] = extract_text_from_file(file_content, filename)
            else:
                # Use Gemini API for other file types
                results[filename] = handle_with_gemini(file_content, filename)

        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
            results[filename] = f"Error: {str(e)}"

    return results
