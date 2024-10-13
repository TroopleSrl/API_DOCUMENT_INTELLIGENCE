import logging
import google.generativeai as genai
import io
import time
import os

# Configure the API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(file_like_object, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(file_like_object, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active before using them."""
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

def handle_with_gemini(file_content, filename):
    """Handles files using Google Generative AI API."""
    mime_type = None
    if filename.lower().endswith('.pdf'):
        mime_type = "application/pdf"
    elif filename.lower().endswith('.png'):
        mime_type = "image/png"

    # Create a BytesIO object from the file content
    file_like_object = io.BytesIO(file_content)

    uploaded_file = upload_to_gemini(file_like_object, mime_type=mime_type)
    wait_for_files_active([uploaded_file])

    # Use default configuration for the model without any custom parameters
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Start a chat session for document analysis
    chat_session = model.start_chat(history=[
        {
            "role": "user",
            "parts": [
                uploaded_file,
                "You're a perfect OCR scanner. Your task is to accurately analyze the images along with the possible documents and return a well-structured text of everything. Check twice the numbers, dates, and names. Don't use prior knowledge. No mistakes allowed. Include everything in order."
            ]
        }
    ])

    response = chat_session.send_message(
        "You're a perfect OCR scanner. Your task is to accurately analyze the images along with the possible documents and return a well-structured text of everything. Check twice the numbers, dates, and names. Don't use prior knowledge. No mistakes allowed. Include everything in order."
    )
    logging.info(f"Gemini API response: {response.text}")
    return response.text
