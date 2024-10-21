from fastapi import FastAPI, Request

from routes.upload import router as upload_router
from routes.chunk import router as chunk_router
from routes.admin import router as register_router
from settings import get_settings

from utils.exceptions import setup_exception_handlers
from database.db import init_db

app = FastAPI()
setup_exception_handlers(app)

app.include_router(upload_router)
app.include_router(chunk_router)
app.include_router(register_router)

# add response header
@app.middleware("http")
async def add_response_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-LLM-MODEL"] = get_settings().GOOGLE_LLM_MODEL
    return response

init_db()
