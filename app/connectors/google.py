import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, File
from io import BytesIO
import time
from settings import get_settings

class GeminiLLM:
    """A Language Learning Model that uses Google Generative AI API."""
    
    def __init__(self):
        genai.configure(api_key=get_settings().GOOGLE_API_KEY.get_secret_value())
        self.generation_config = get_settings().GOOGLE_MODEL_CONFIG
        self.system_prompt = get_settings().SYSTEM_PROMPT
        self.model = genai.GenerativeModel(
            model_name=get_settings().GOOGLE_LLM_MODEL,
            system_instruction=self.system_prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        self.files = []
    
    def upload_file(self, file_like_object: BytesIO, mime_type: str, wait: bool = True) -> File:
        file = genai.upload_file(file_like_object, mime_type=mime_type)
        if wait: file = self.wait_for_file(file)
        self.files.append(file)
        print(file.to_dict())
        return file

    def remove_file(self, file: File) -> None:
        genai.delete_file(file.name)
        self.files.remove(file)
        
    def wait_for_file(self, file: File) -> File:
        while file.state.name == "PROCESSING":
            time.sleep(2)
            file = genai.get_file(file.name)

        if file.state.name != "ACTIVE": raise Exception(f"File {file.name} failed to process")
        return file

    def chat(self, message: str) -> str:
        try:
            response = self.model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": self.files,
                    }
                ]
            ).send_message(message)
            return response.text
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred."