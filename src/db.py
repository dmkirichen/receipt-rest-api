from sqlmodel import SQLModel, create_engine, Session
from decimal import Decimal

from models.user import User
from models.item import Item
from models.item_group import ItemGroup
from models.receipt import Receipt

# TODO move all this to .env
DB_USERNAME = "admin"
DB_PASSWORD = "admin"
DB_URL = "localhost"
DB_PORT = "5432"
DB_NAME = "receipt_db"

DATABASE_URL = f"postgresql+pg8000://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"

engine = create_engine(url=DATABASE_URL)


def create_dummy_data():
    global engine

    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:    
        # Creating ORM objects for users
        # user_1 will have password "secret", user_2 will have "secret"
        user_1 = User(username="aalice", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="Alice Ambercromby")
        user_2 = User(username="bobbyb", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="Bob Bildgewater")

        # Need to add users to database before creating receipt objects
        session.add(user_1)
        session.add(user_2)
        session.commit()

        # Creating ORM objects for items
        item_1 = Item(name="Bread", price=21)
        item_2 = Item(name="Butter", price=35)
        item_3 = Item(name="Bacon", price=58.5)
        
        # Need to add items to database before creating item groups and receipt
        session.add(item_1)
        session.add(item_2)
        session.add(item_3)
        session.commit()

        # Creating ORM objects for receipts
        receipt_1 = Receipt(
            user_id=user_1.id,
            payment_type="cash",
            total_payment=Decimal(200)
        )
        receipt_2 = Receipt(
            user_id=user_2.id,
            payment_type="card",
            total_payment=Decimal(300)
        )

        # Populating database with receipts objects
        session.add(receipt_1)
        session.add(receipt_2)
        session.commit()
        
        # Creating ORM objects for item groups
        item_group_1 = ItemGroup(
            item_id=item_1.id,
            quantity=2.0,
            total_price=item_1.price * Decimal(2.0),
            receipt_id=receipt_1.id
        )
        item_group_2 = ItemGroup(
            item_id=item_2.id,
            quantity=3.0,
            total_price=item_2.price * Decimal(3.0),
            receipt_id=receipt_1.id
        )
        item_group_3 = ItemGroup(
            item_id=item_2.id,
            quantity=2.0,
            total_price=item_2.price * Decimal(2.0),
            receipt_id=receipt_2.id
        )
        item_group_4 = ItemGroup(
            item_id=item_3.id,
            quantity=3.0,
            total_price=item_3.price * Decimal(3.0),
            receipt_id=receipt_2.id
        )

        # Populating database with item groups objects
        session.add(item_group_1)
        session.add(item_group_2)
        session.add(item_group_3)
        session.add(item_group_4)
        session.commit()

        # Updating total price in receipt objects
        receipt_1.total_price = item_group_1.total_price + item_group_2.total_price
        receipt_2.total_price = item_group_3.total_price + item_group_4.total_price
        session.add(receipt_1)
        session.add(receipt_2)
        session.commit()

        # Show created ORM objects
        session.refresh(user_1)
        session.refresh(user_2)
        session.refresh(item_1)
        session.refresh(item_2)
        session.refresh(item_3)
        session.refresh(item_group_1)
        session.refresh(item_group_2)
        session.refresh(item_group_3)
        session.refresh(item_group_4)
        session.refresh(receipt_1)
        session.refresh(receipt_2)

        print(f"Created user: {user_1}")
        print(f"Created user: {user_2}")
        print(f"Created item: {item_1}")
        print(f"Created item: {item_2}")
        print(f"Created item: {item_3}")
        print(f"Created item group: {item_group_1}")
        print(f"Created item group: {item_group_2}")
        print(f"Created item group: {item_group_3}")
        print(f"Created item group: {item_group_4}")
        print(f"Created receipt: {receipt_1}")
        print(f"Created receipt: {receipt_2}")


if __name__ == '__main__':
    create_dummy_data()
