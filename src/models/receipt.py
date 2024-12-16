from decimal import Decimal
from typing import Optional, List
from sqlmodel import Field, SQLModel, Column, Enum
from datetime import datetime

from .item_group import ItemGroupCreate, ItemGroupPublic
from utils import PaymentType

class Receipt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    payment_type: str = Field(sa_column=Column(PaymentType, default="cash"))
    total_price: Optional[Decimal] = Field(default=None)
    total_payment: Decimal = Field(default=0, max_digits=8, decimal_places=2)

class ReceiptCreate(SQLModel):
    payment_type: str = Field(sa_column=Column(PaymentType, default="cash"))
    item_groups: List["ItemGroupCreate"]
    total_payment: Decimal

class ReceiptPublic(SQLModel):
    id: int
    created_at: datetime
    user_full_name: str
    item_groups: List["ItemGroupPublic"]
    payment_type: str
    total_price: Decimal
    total_payment: Decimal
    payment_change: Decimal

class ReceiptFilter:
    created_after: Optional[datetime]
    created_before: Optional[datetime]
    total_price_from: Optional[Decimal]
    total_price_to: Optional[Decimal]
    payment_types: Optional[Enum]
