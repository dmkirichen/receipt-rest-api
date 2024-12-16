"""
Left to add
[ ] correct filter by created
[ ] correct filter by price
[ ] correct filter by payment type
[ ] pagination
[ ] docs for API
[ ] README file with launch instructions
[ ] proper move of variables to .env
[ ] docker compose

Additional task (pytest):
[ ] test registration
[ ] test authorization
[ ] test creation of receipt
[ ] test getting receipt
[ ] test public getting receipt
[ ] test unallowed requests
"""
import logging
from typing import Annotated, List, Optional
from datetime import timedelta, datetime
from decimal import Decimal

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_filter import FilterDepends
from sqlmodel import Enum

from security import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user

from models.user import User, UserPublic, UserCreate
from models.token import Token
from models.item import Item
from models.receipt import ReceiptCreate, ReceiptPublic, ReceiptFilter

from db_operations import read_all_receipts, read_receipt, add_new_user, get_user, add_new_receipt
from utils import form_receipt_string, PaymentType


app = FastAPI()

LOG = logging.getLogger(__name__)
LOG.info("API is starting up")


@app.get("/")
def app_get():
    return {'info': 'FastAPI Working'}


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    return current_user


@app.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate):
    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with such username already exists"
        )
    new_user = add_new_user(user)
    return new_user


@app.get("/receipts", response_model=list[ReceiptPublic])
def get_receipts(
    current_user: Annotated[User, Depends(get_current_user)],
    created_after: Optional[datetime],
    created_before: Optional[datetime],
    total_price_from: Optional[Decimal],
    total_price_to: Optional[Decimal],
    payment_types: Optional[Enum]
) -> List[ReceiptPublic]:
    receipt_filter = ReceiptFilter(
        created_after=created_after, 
        created_before=created_before, 
        total_price_from=total_price_from, 
        total_price_to=total_price_to, 
        payment_types=payment_types
    )
    return read_all_receipts(
        user_id=current_user.id,
        receipt_filter=receipt_filter
    )


@app.get("/receipts/{receipt_id}")
def get_receipt(
    receipt_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
) -> ReceiptPublic:
    return read_receipt(receipt_id=receipt_id)


@app.post("/receipt")
def create_receipt(
    receipt: ReceiptCreate, 
    current_user: Annotated[User, Depends(get_current_user)]
) -> ReceiptPublic:
    return add_new_receipt(receipt, current_user)


@app.get("/receipts/print/{receipt_id}")
def print_receipt(
    current_user: Annotated[User, Depends(get_current_user)],
    receipt_id: int, 
    line_width: int = 30
):
    receipt = read_receipt(receipt_id=receipt_id)
    result = form_receipt_string(receipt, line_width)
    return HTMLResponse(content=result)


@app.delete("/receipts/{receipt_id}")
def delete_receipt(receipt_id: int):
    return {'info': f'trying to delete {receipt_id}'}
