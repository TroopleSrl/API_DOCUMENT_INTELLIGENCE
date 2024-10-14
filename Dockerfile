FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./app /app/app
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --upgrade --no-cache-dir
