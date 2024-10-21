docker compose --profile dev up -d &&
cd app && sh prestart.sh && uvicorn main:app --port 8000 --workers 1 --reload