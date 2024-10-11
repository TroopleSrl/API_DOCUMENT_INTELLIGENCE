from fastapi import APIRouter, UploadFile
from typing import List
import os
from app.functions.parser import extract_text_from_file
from app.connectors.gemini import handle_with_gemini

# Create a router instance
router = APIRouter()

@router.post("/uploadfiles/")
async def upload_files(files: List[UploadFile]):
    results = {}

    # Ensure the 'temp' directory exists
    os.makedirs('./temp', exist_ok=True)

    for file in files:
        try:
            filename = file.filename
            print(f"Processing file: {filename}")

            # Determine file handling based on file extension
            if filename.lower().endswith(('.docx', '.xlsx', '.eml')):
                # Process file with local extraction logic
                file_content = await file.read()
                results[filename] = extract_text_from_file(file_content, filename)
            else:
                # Use Gemini API for other file types
                temp_file = f"./temp/{filename}"
                with open(temp_file, "wb") as temp:
                    temp.write(await file.read())
                results[filename] = handle_with_gemini(temp_file)

        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
            results[filename] = f"Error: {str(e)}"

    return results
