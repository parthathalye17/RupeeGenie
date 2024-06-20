from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import uuid
import uvicorn

app = FastAPI()

# Middleware to allow cross-origin requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdtam5hb2ZvcHB2anF0bnJucmF4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTczMzA0MTYsImV4cCI6MjAzMjkwNjQxNn0.nUkBMwoZkcGKiH4_bqCkmFVwXpOnm8W_q77zcFAf6l0"

supabase: Client = create_client("https://gmjnaofoppvjqtnrnrax.supabase.co", SUPABASE_API_KEY)

# Pydantic models for request bodies
class SignUpRequest(BaseModel):
    email: str
    password: str
    phone_number: str
    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    city: str
    state: str
    country: str
    zip_code: str
    registration_date: str
    language: str
    balance: float
    salary: float
    occupation: str

class AccountRequest(BaseModel):
    account_type: str
    balance: float
    created_at: str
    status: str
    branch_name: str
    ifsc_code: str
    interest_rate: float
    overdraft_limit: float

class UPIRequest(BaseModel):
    created_at: str
    status: str

class CreditCardRequest(BaseModel):
    card_number: str
    cardholder_name: str
    expiration_date: str
    cvv: str
    credit_limit: float
    balance: float
    status: str
    issued_at: str
    billing_address: str
    reward_points: float
    interest_rate: float

class TransactionRequest(BaseModel):
    transaction_type: str
    amount: float
    transaction_date: str
    merchant: str
    status: str
    description: str
    category: str
    sender_account_id: str
    receiver_account_id: str

@app.post("/signup/")
async def sign_up(sign_up_request: SignUpRequest):
    auth_response = supabase.auth.sign_up({
        'email': sign_up_request.email,
        'password': sign_up_request.password
    })

    if 'error' in auth_response:
        raise HTTPException(status_code=400, detail=auth_response['error'])

    auth_id = auth_response['data']['user']['id']

    user_data = sign_up_request.dict()
    user_data['auth_id'] = auth_id
    # Break the code here
    response = supabase.from_('users_b').insert(user_data).execute()

    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])

    return {"message": "User signed up successfully", "auth_id": auth_id}

@app.post("/add_account/")
async def add_account(auth_id: str, account_request: AccountRequest):
    user_response = supabase.from_('users_b').select('*').eq('auth_id', auth_id).execute()
    
    if len(user_response['data']) == 0:
        raise HTTPException(status_code=404, detail="User not found")

    account_data = account_request.dict()
    account_data['account_id'] = str(uuid.uuid4())
    
    account_response = supabase.from_('bank_accounts').insert(account_data).execute()
    
    if 'error' in account_response:
        raise HTTPException(status_code=400, detail=account_response['error'])

    user_data = user_response['data'][0]
    user_data['account_id'] = account_data['account_id']
    
    supabase.from_('users_b').update(user_data).eq('auth_id', auth_id).execute()

    return {"message": "Account added successfully", "account_id": account_data['account_id']}

@app.post("/add_upi/")
async def add_upi(auth_id: str, upi_request: UPIRequest):
    user_response = supabase.from_('users_b').select('*').eq('auth_id', auth_id).execute()
    
    if len(user_response['data']) == 0:
        raise HTTPException(status_code=404, detail="User not found")

    upi_data = upi_request.dict()
    upi_data['upi_id'] = str(uuid.uuid4())

    upi_response = supabase.from_('upi_ids').insert(upi_data).execute()
    
    if 'error' in upi_response:
        raise HTTPException(status_code=400, detail=upi_response['error'])

    user_data = user_response['data'][0]
    user_data['upi_id'] = upi_data['upi_id']
    
    supabase.from_('users_b').update(user_data).eq('auth_id', auth_id).execute()

    return {"message": "UPI added successfully", "upi_id": upi_data['upi_id']}

@app.post("/add_credit_card/")
async def add_credit_card(account_id: str, credit_card_request: CreditCardRequest):
    credit_card_data = credit_card_request.dict()
    credit_card_data['card_id'] = str(uuid.uuid4())
    credit_card_data['account_id'] = account_id

    response = supabase.from_('credit_cards').insert(credit_card_data).execute()

    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])

    return {"message": "Credit card added successfully", "card_id": credit_card_data['card_id']}

@app.post("/add_transaction/")
async def add_transaction(transaction_request: TransactionRequest):
    transaction_data = transaction_request.dict()
    transaction_data['transaction_id'] = str(uuid.uuid4())

    response = supabase.from_('transactions').insert(transaction_data).execute()

    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])

    return {"message": "Transaction added successfully", "transaction_id": transaction_data['transaction_id']}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
