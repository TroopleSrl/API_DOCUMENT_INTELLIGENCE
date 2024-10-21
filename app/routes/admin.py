from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta

from sqlmodel import select
from sqlalchemy.orm import selectinload
from database.db import get_session
from database.models import Client, Key 
from utils.authorization import is_admin, encode_fernet

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(is_admin)] # every admin route will require the X-ADMIN-TOKEN header
)

@router.get("/clients")
def get_clients():
    with get_session() as session:
        return session.exec(select(Client)).all()
    
@router.post("/register/client")
def register_client(name: str):

    with get_session() as session:

        existing_client = session.exec(
            select(Client).where(Client.name == name)
        ).first()

        if existing_client: raise HTTPException(status_code=400, detail="Client already registered")
        
        new_client = Client(name=name)
        session.add(new_client)
        session.commit()
        
        return new_client
    
@router.post("/register/key")
def register_key(client_name: str, expires: int = 365, quota: int = 1000):

    with get_session() as session:

        existing_client = session.exec(
            select(Client).where(Client.name == client_name)
        ).first()

        if not existing_client: raise HTTPException(status_code=400, detail="Client not found")

        new_key = Key(
            client_id=existing_client.id, 
            expiration_date=datetime.now() + timedelta(days=expires), 
            quota=quota
        )
        session.add(new_key)
        session.commit()
        return {"key": new_key, "token": encode_fernet(new_key.client_id, new_key.id)}