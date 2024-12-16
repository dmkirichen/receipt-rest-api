from typing import Optional, List
from decimal import Decimal

from fastapi import HTTPException
from sqlmodel import Session, select

from db import engine
from models.item import Item
from models.item_group import ItemGroup, ItemGroupPublic
from models.receipt import Receipt, ReceiptCreate, ReceiptPublic, ReceiptFilter
from models.user import User, UserCreate
from utils import get_password_hash


def get_user(username: str) -> Optional[User]:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        return user
    

def add_new_user(user: UserCreate) -> User:
    with Session(engine) as session:
        new_user = User(
            username=user.username, 
            hashed_password=get_password_hash(user.password), 
            full_name=user.full_name
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user


def read_all_receipts(
        user_id: int, receipt_filter: ReceiptFilter
) -> List[ReceiptPublic]:
    with Session(engine) as session:
        statement = select(Receipt).where(Receipt.user_id == user_id)
        query_filter = receipt_filter.filter(statement)
        results = session.exec(query_filter)
        receipt_ids = [result.id for result in results.all()]

        results = []
        for receipt_id in receipt_ids:
            results.append(read_receipt(receipt_id))
        return results


def read_receipt(receipt_id: int) -> ReceiptPublic:
    with Session(engine) as session:
        statement = select(Receipt).where(Receipt.id == receipt_id)
        results = session.exec(statement)
        receipt = results.first()

        # Adding info about item groups
        statement = select(ItemGroup).where(
            ItemGroup.receipt_id == receipt.id
        )
        results = session.exec(statement)
        item_groups = results.all()
        item_groups_public = []
        for item_group in item_groups:
            item = session.exec(select(Item).where(
                Item.id == item_group.item_id
            )).first()
            item_groups_public.append(
                ItemGroupPublic(
                    item_name=item.name,
                    item_price=item.price,
                    quantity=item_group.quantity, 
                    total_price=item_group.total_price
                )
            )

        # Adding info about user
        statement = select(User).where(User.id == receipt.user_id)
        user_full_name = session.exec(statement).first().full_name

        result = ReceiptPublic(
            id=receipt.id,
            created_at=receipt.created_at,
            user_full_name=user_full_name,
            item_groups=item_groups_public,
            payment_type=receipt.payment_type,
            total_price=receipt.total_price,
            total_payment=receipt.total_payment,
            payment_change=receipt.total_payment-receipt.total_price,
        )
        return result
    
def add_new_receipt(receipt: ReceiptCreate, user: User, filter: ReceiptFilter) -> ReceiptPublic:
    with Session(engine) as session:
        for item_group in receipt.item_groups:
            # Validate input in item groups
            item = item_group.item
            quantity = item_group.quantity
            # TODO validate input before creating receipt for it

        # If everything is okay we may proceed with creation of a Receipt
        new_receipt = Receipt(
            user_id=user.id,
            payment_type=receipt.payment_type,
            total_payment=receipt.total_payment,
        )
        session.add(new_receipt)
        session.commit()
        session.refresh(new_receipt)

        # Now we create corresponding item groups for this receipt
        total_price = Decimal(0)
        for item_group_create in receipt.item_groups:
            item = session.exec(
                select(Item).where(Item.name == item_group_create.item.name)
            ).first()
            item_group_price = item.price * item_group_create.quantity
            item_group = ItemGroup(
                item_id=item.id,
                quantity=item_group_create.quantity,
                total_price=item_group_price,
                receipt_id=new_receipt.id
            )
            session.add(item_group)
            session.commit()

            total_price += item_group_price

        # Update total price of created receipt one last time
        new_receipt.total_price = total_price
        session.add(new_receipt)
        session.commit()
        return read_receipt(new_receipt.id)
        