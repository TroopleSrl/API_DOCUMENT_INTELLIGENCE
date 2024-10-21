from database.db import get_session
from database.models import Client, Key
from sqlmodel import select

def get_key_if_client(client_id: str, key_id: str):
    with get_session() as db:
        query = select(Key).where(Key.client_id == client_id).where(Key.id == key_id)
        result = db.exec(query).first()
        return result