from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from sqlmodel import select, Session
from database.db import get_db
from database.models import Client, Key 

router = APIRouter()

@router.post("/register")
def register_client(name: str, db: Session = Depends(get_db)):
    # Check if client already exists
    existing_client = db.exec(
        select(Client).where(Client.name == name)
    ).first()

    if existing_client:
        raise HTTPException(status_code=400, detail="Client already registered")
    
    # Create new client
    new_client = Client(name=name)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    # Create an API key for the new client
    new_key = Key(
        client_id=new_client.id, 
        expiration_date=datetime.now() + timedelta(days=30),  # Key valid for 30 days
        quota=1000  
    )

    db.add(new_key)
    db.commit()
    db.refresh(new_key)

    return {"client_id": new_client.id, "api_key": new_key.id}
