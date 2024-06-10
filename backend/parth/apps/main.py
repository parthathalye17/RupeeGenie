from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import random
import secrets
from .models import TransactionForm, UserForm, AccountForm, UpiIdForm, TransferForm, CreditCardForm, Token

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_token(user_id: int) -> str:
    token = secrets.token_hex(16)
    response = supabase.table("tokens").insert({"token": token, "user_id": user_id}).execute()
    if raise_when_api_error(response=response) == 'error':
        raise HTTPException(status_code=500, detail="Error creating token")
    return token

def authenticate_user(username: str, password: str):
    user_response = supabase.table("users").select("*").eq("username", username).execute()
    if not user_response.data:
        return False
    user = user_response.data[0]
    if not verify_password(password, user['password_hashed']):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_response = supabase.table("tokens").select("*").eq("token", token).execute()
    if not token_response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = token_response.data[0]
    user_response = supabase.table("users").select("*").eq("id", token_data["user_id"]).execute()
    if not user_response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_response.data[0]

@app.post("/register", response_model=dict)
def register_user(
    username: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...)
):
    if password != password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    hashed_password = get_password_hash(password)
    user_data = {
        "username": username,
        "password_hashed": hashed_password,
        "email": email,
        "phone_number": phone_number,
        "registration_date": datetime.utcnow().isoformat(),
        "is_active": True,
        "is_verified": False,
    }
    response = supabase.table("users").insert(user_data).execute()
    raise_when_api_error(response)
    return {"msg": "User registered successfully"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_token(user["id"])
    return {"token": token, "user_id": user["id"]}

@app.post("/profile", response_model=dict)
def create_profile(
    email: Optional[str] = Form(None),
    phone_number: str = Form(...),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    zip_code: Optional[str] = Form(None),
    preferred_language: Optional[str] = Form(None),
    salary: Optional[float] = Form(None),
    years_to_retirement: Optional[int] = Form(None),
    employment_status: Optional[str] = Form(None),
    marital_status: Optional[str] = Form(None),
    dependents: Optional[int] = Form(None),
    income_source: Optional[str] = Form(None),
    occupation: Optional[str] = Form(None),
    investment_preferences: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    if len(phone_number) != 10 or not phone_number.isdigit():
        raise HTTPException(status_code=400, detail="Inappropriate phone number")

    user_data = {
        "email": email,
        "phone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "address": address,
        "city": city,
        "state": state,
        "country": country,
        "zip_code": zip_code,
        "preferred_language": preferred_language,
        "salary": salary,
        "years_to_retirement": years_to_retirement,
        "employment_status": employment_status,
        "marital_status": marital_status,
        "dependents": dependents,
        "income_source": income_source,
        "occupation": occupation,
        "investment_preferences": investment_preferences,
        "last_login": datetime.utcnow().isoformat(),
    }
    response = supabase.table("users").update(user_data).eq("id", current_user["id"]).execute()
    raise_when_api_error(response)
    return response.data

@app.post("/accounts/", response_model=dict)
def create_account(
    user_id: int = Form(...),
    account_type: str = Form(...),
    account_number: str = Form(...),
    branch_name: str = Form(...),
    ifsc_code: str = Form(...),
    interest_rate: float = Form(...),
    overdraft_limit: Optional[float] = Form(0.0),
    current_user: dict = Depends(get_current_user)
):
    account = AccountForm(
        user_id=user_id,
        account_type=account_type,
        account_number=account_number,
        branch_name=branch_name,
        ifsc_code=ifsc_code,
        interest_rate=interest_rate,
        overdraft_limit=overdraft_limit
    )
    account_data = account.dict()
    response = supabase.table("bank_accounts").insert(account_data).execute()
    raise_when_api_error(response)
    return response.data

@app.post("/transactions/", response_model=dict)
def create_transaction(
    account_id: int = Form(...),
    card_id: Optional[int] = Form(None),
    user_id: int = Form(...),
    transaction_type: str = Form(...),
    amount: float = Form(...),
    merchant: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    transaction = TransactionForm(
        account_id=account_id,
        card_id=card_id,
        user_id=user_id,
        transaction_type=transaction_type,
        amount=amount,
        merchant=merchant,
        description=description,
        category=category
    )
    account_response = supabase.table("bank_accounts").select("*").eq("id", transaction.account_id).execute()
    raise_when_api_error(account_response)
    account = account_response.data[0] if account_response.data else None
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    new_balance = account["balance"] + transaction.amount
    update_response = supabase.table("bank_accounts").update({"balance": new_balance}).eq("id", transaction.account_id).execute()
    raise_when_api_error(update_response)
    
    transaction_data = transaction.dict()
    trans_response = supabase.table("transactions").insert(transaction_data).execute()
    raise_when_api_error(trans_response)
    return trans_response.data

@app.post("/transfer/", response_model=dict)
def transfer_money(
    sender_account_id: int = Form(...),
    receiver_account_id: int = Form(...),
    amount: float = Form(...),
    current_user: dict = Depends(get_current_user)
):
    transfer = TransferForm(sender_account_id=sender_account_id, receiver_account_id=receiver_account_id, amount=amount)
    sender_response = supabase.table("bank_accounts").select("*").eq("id", transfer.sender_account_id).execute()
    raise_when_api_error(sender_response)
    receiver_response = supabase.table("bank_accounts").select("*").eq("id", transfer.receiver_account_id).execute()
    raise_when_api_error(receiver_response)
    
    sender_account = sender_response.data[0] if sender_response.data else None
    receiver_account = receiver_response.data[0] if receiver_response.data else None
    
    if not sender_account or not receiver_account:
        raise HTTPException(status_code=404, detail="Account not found")

    if sender_account["balance"] < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    new_sender_balance = sender_account["balance"] - transfer.amount
    new_receiver_balance = receiver_account["balance"] + transfer.amount

    update_sender_response = supabase.table("bank_accounts").update({"balance": new_sender_balance}).eq("id", transfer.sender_account_id).execute()
    raise_when_api_error(update_sender_response)
    update_receiver_response = supabase.table("bank_accounts").update({"balance": new_receiver_balance}).eq("id", transfer.receiver_account_id).execute()
    raise_when_api_error(update_receiver_response)

    sender_transaction_data = {"amount": -transfer.amount, "account_id": transfer.sender_account_id, "user_id": sender_account["user_id"], "transaction_type": "transfer_out"}
    receiver_transaction_data = {"amount": transfer.amount, "account_id": transfer.receiver_account_id, "user_id": receiver_account["user_id"], "transaction_type": "transfer_in"}

    sender_trans_response = supabase.table("transactions").insert(sender_transaction_data).execute()
    raise_when_api_error(sender_trans_response)
    receiver_trans_response = supabase.table("transactions").insert(receiver_transaction_data).execute()
    raise_when_api_error(receiver_trans_response)

    return {"msg": "Transfer successful"}

@app.post("/upi_ids/", response_model=dict)
def create_upi_id(
    user_id: int = Form(...),
    account_id: int = Form(...),
    upi_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    upi_id_form = UpiIdForm(user_id=user_id, account_id=account_id, upi_id=upi_id)
    upi_data = upi_id_form.dict()
    response = supabase.table("upi_ids").insert(upi_data).execute()
    raise_when_api_error(response)
    return response.data

@app.post("/credit_cards/", response_model=dict)
def create_credit_card(
    user_id: int = Form(...),
    card_number: str = Form(...),
    cardholder_name: str = Form(...),
    expiry_date: str = Form(...),
    cvv: str = Form(...),
    credit_limit: float = Form(...),
    billing_address: str = Form(...),
    interest_rate: float = Form(...),
    current_user: dict = Depends(get_current_user)
):
    credit_card_form = CreditCardForm(
        user_id=user_id,
        card_number=card_number,
        cardholder_name=cardholder_name,
        expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d').date(),
        cvv=cvv,
        credit_limit=credit_limit,
        billing_address=billing_address,
        interest_rate=interest_rate
    )
    card_data = credit_card_form.dict()
    response = supabase.table("credit_cards").insert(card_data).execute()
    raise_when_api_error(response)
    return response.data

def raise_when_api_error(response):
    if response.get('error'):
        raise HTTPException(status_code=400, detail=f"API Error: {response['error']['message']}")
    return response.data
