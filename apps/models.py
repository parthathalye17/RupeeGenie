from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserForm(BaseModel):
    username: str
    password: str
    email: str
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]

class AccountForm(BaseModel):
    user_id: int
    account_number: str
    account_type: str
    branch_name: str
    ifsc_code: str
    interest_rate: float
    overdraft_limit: Optional[float] = 0.0

class TransactionForm(BaseModel):
    account_id: int
    card_id: Optional[int]
    user_id: int
    transaction_type: str
    amount: float
    merchant: str
    description: Optional[str]
    category: Optional[str]

class TransferForm(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: float

class UpiIdForm(BaseModel):
    user_id: int
    account_id: int
    upi_id: str

class CreditCardForm(BaseModel):
    user_id: int
    card_number: str
    cardholder_name: str
    expiry_date: date
    cvv: str
    credit_limit: float
    billing_address: str
    reward_points: Optional[float] = 0.0
    interest_rate: float

class Token(BaseModel):
    token: str
    user_id: int
