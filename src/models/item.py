from decimal import Decimal
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: Decimal = Field(default=0, max_digits=8, decimal_places=2)

class ItemGet(SQLModel):
    name: str
