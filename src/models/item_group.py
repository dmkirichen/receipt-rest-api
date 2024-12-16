from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel

from .item import ItemGet


class ItemGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="item.id")
    quantity: Decimal = Field(default=0, max_digits=8, decimal_places=2)
    total_price: Decimal = Field(default=0, max_digits=8, decimal_places=2)
    receipt_id: int = Field(default=None, foreign_key="receipt.id")

class ItemGroupCreate(SQLModel):
    item: ItemGet
    quantity: Decimal

class ItemGroupPublic(SQLModel):
    item_name: str
    item_price: Decimal
    quantity: Decimal
    total_price: Decimal
