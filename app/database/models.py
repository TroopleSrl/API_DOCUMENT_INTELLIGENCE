from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

# Client Table
class Client(SQLModel, table=True):
    __tablename__ = "clients"    

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    keys: List["Key"] = Relationship(back_populates="client")

# Keys Table
class Key(SQLModel, table=True):
    __tablename__ = "keys"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    client_id: UUID = Field(foreign_key="clients.id", nullable=False)
    expiration_date: datetime = Field(nullable=False)
    last_used: Optional[datetime] = None
    quota: int = Field(default=1000, nullable=False)

    client: "Client" = Relationship(back_populates="keys")
    requests: List["Request"] = Relationship(back_populates="key")

# Requests Table
class Request(SQLModel, table=True):
    __tablename__ = "requests"  

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    key_id: UUID = Field(foreign_key="keys.id", nullable=False)
    endpoint: str = Field(nullable=False)
    credits: int = Field(nullable=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    key: "Key" = Relationship(back_populates="requests")
