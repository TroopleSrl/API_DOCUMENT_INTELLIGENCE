FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./app /app/app
COPY ./app/requirements.txt /app/requirements.txt
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    && apt-get clean

RUN pip install -r /app/requirements.txt --upgrade --no-cache-dir

