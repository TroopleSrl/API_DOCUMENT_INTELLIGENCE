from functools import lru_cache
from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ignore env variables that are not in the model
    model_config = SettingsConfigDict(env_file=".env", case_insensitive=True, extra="ignore", env_prefix="TROOPLE__")
    
    ADMIN_TOKEN: SecretStr
    FERNET_KEY: SecretStr = "4SNd1Twp3OWR-G2Qd6wXDkDyjz1FHDQMxecva4tVIDk="

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    GOOGLE_API_KEY: SecretStr
    GOOGLE_LLM_MODEL: str = "gemini-1.5-flash"
    GOOGLE_MODEL_CONFIG : dict = {
        "temperature": 0,
        "candidate_count": 1
    }

    DATABASE_URL : PostgresDsn

    # OPENAI_API_KEY: SecretStr

    SYSTEM_PROMPT : str = "You are an AI expert specializing in Optical Character Recognition (OCR) and text extraction from images and scanned documents."
    USER_PROMPT : str = """
Your tasks are:

1. Perform thorough OCR on all pages of the provided document or image.

2. Extract ALL written text, ensuring no information is missed.

3. Double-check and verify the following elements for consistency across the entire document:
   a. Names
   b. Numbers
   c. Dates
   d. People mentioned
   e. Checkboxes (checked or unchecked)
   f. Phone numbers

4. Ensure logical consistency of dates and names throughout the document.

5. Verify that all extracted information is coherent and makes sense in context.

6. Provide a comprehensive and accurate transcription of the entire document without page separation.

7. Return the transcription in a clean, readable format. If there are several languages present in the document, separate the text by language.

Remember: Accuracy, completeness, and consistency are your top priorities. Do not omit any text, no matter how insignificant it may seem.
Return only the text without explanations or comments.
""".strip()

@lru_cache
def get_settings(what: str = "") -> Settings: 
    if what: return getattr(Settings(), what)
    return Settings()