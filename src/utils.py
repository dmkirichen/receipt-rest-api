from passlib.context import CryptContext
from models.receipt import ReceiptPublic
from sqlmodel import Enum


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

PaymentType = Enum("cash", "card", name="PaymentType")


def verify_password(plain_password, hashed_password):    
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def form_receipt_string(receipt: ReceiptPublic, line_width: int):
    result = f"\n{receipt.user_full_name:^{line_width}}\n"
    result += "=" * line_width
    add_divider = False
    for item_group in receipt.item_groups:
        if add_divider:
            result += "\n" + "-" * line_width
        add_divider = True
    
        result += f"\n{f'{item_group.quantity:.2f} x {item_group.item_price:.2f}':<{line_width}}"
        result += f"\n{item_group.item_name:<{line_width//2}}"
        result += f"{item_group.total_price:>{line_width//2}}\n"

    result += "=" * line_width
    result += f"\n{receipt.created_at.strftime('%d.%m.%y %H:%M'):^{line_width}}"
    result += f"\n{'Thank you for your purchase':^{line_width}}\n"
    return result
