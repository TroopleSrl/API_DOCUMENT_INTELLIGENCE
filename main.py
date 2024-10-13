from fastapi import FastAPI
from app.routes.upload_files import router as upload_router

app = FastAPI()

app.include_router(upload_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
