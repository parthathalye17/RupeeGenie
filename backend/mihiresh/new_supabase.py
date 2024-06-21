from fastapi import FastAPI,File,UploadFile,Form, Request, HTTPException, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import uuid
import uvicorn
import random
import string
from datetime import date, datetime

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



class UserBRequest(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    address: str
    city: str
    state: str
    country: str
    zip_code: str
    registration_date: date
    language: str
    balance: float
    salary: float
    occupation: str

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




def generate_varchar_id(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@app.post("/add_users_b")
async def add_users(
    email: str = Form(...),
    password: str = Form(...),
    phone_number: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    country: str = Form(...),
    zip_code: str = Form(...),
    registration_date: str = Form(...),
    language: str = Form(...),
    balance: float = Form(...),
    salary: float = Form(...),
    occupation: str = Form(...)
):
    try:
        
        data = {
            "email": email,
            "password": password
        }
        response = supabase.auth.sign_in_with_password(data)
        auth_id = response.user.id
        print(f"User_id: {auth_id}\n")
        account_id = generate_varchar_id()
        upi_id = generate_varchar_id()
        print(f"\nAccount: {account_id}\n\nUpi: {upi_id}\n\n")
        date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y").strftime("%Y-%m-%d")
        registration_date = datetime.strptime(registration_date, "%d/%m/%Y").strftime("%Y-%m-%d")

        user_b_data = {
            "auth_id": auth_id,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "zip_code": zip_code,
            "registration_date": registration_date,
            "language": language,
            "balance": balance,
            "salary": salary,
            "occupation": occupation,
            "account_id": account_id,
            "upi_id": upi_id,
            "email": email
        }

        response = supabase.table('users_b').insert(user_b_data).execute()
        return JSONResponse(content={"message": "Done", "success": True}, status_code=200)

    except Exception as e:
        print(f"Error is:\n\n{e}\n")
        return JSONResponse(content={"message": "failure"}, status_code=500)



@app.post("/add_account")
async def add_account(
    email: str = Form(...),
    password: str = Form(...),
    account_type: str = Form(...),
    balance: float = Form(...),
    created_at: str = Form(...),
    status: str = Form(...),
    branch_name: str = Form(...),
    ifsc_code: str = Form(...),
    interest_rate: float = Form(...),
    overdraft_limit: float = Form(...)
):
    try:
        try:
            data = {
                "email": email,
                "password": password
            }
            response = supabase.auth.sign_in_with_password(data)
            auth_id = response.user.id
        except Exception as e:
            print(f"\nError:\n\n{e}")
            return JSONResponse(content={"message": "failure while getting auth_id"}, status_code=500)

        # user_response = supabase.from_('users_b').select('*').eq('auth_id', auth_id).execute()
        try:
            user_response = supabase.from_('users_b').select('account_id').eq('auth_id', auth_id).execute()
            account_id = user_response.data[0]['account_id']
            print(f"Account id is: {account_id}")
        except Exception as e:
            print(f"\nError:\n\n{e}")
            return JSONResponse(content={"message": "failure while getting account_id"}, status_code=500)

        created_at = datetime.strptime(created_at, "%d/%m/%Y").strftime("%Y-%m-%d")
        
        account_data = {
            "account_id": account_id,
            "account_type": account_type,
            "balance": balance,
            "created_at": created_at,
            "status": status,
            "branch_name": branch_name,
            "ifsc_code": ifsc_code,
            "interest_rate": interest_rate,
            "overdraft_limit": overdraft_limit
        }

        account_response = supabase.from_('bank_accounts').insert(account_data).execute()

        return JSONResponse(content={"message": "Done", "account_id": account_id, "success": True}, status_code=200)
    
    except Exception as e:
        print(f"\nError:\n\n{e}")
        return JSONResponse(content={"message": "failure"}, status_code=500)
    
    

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
