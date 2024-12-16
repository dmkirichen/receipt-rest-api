from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: str
    hashed_password: str


class UserPublic(SQLModel):
    username: str
    full_name: str


class UserCreate(SQLModel):
    username: str
    full_name: str
    password: str
