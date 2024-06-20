from fastapi import FastAPI,File,UploadFile,Form, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from supabase import create_client, Client
import json
# from bhashini import text_to_speech, transcribe, translation
# from chat_bot import chatbot_response

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")



print(f"URL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_KEY}")

SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdtam5hb2ZvcHB2anF0bnJucmF4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTczMzA0MTYsImV4cCI6MjAzMjkwNjQxNn0.nUkBMwoZkcGKiH4_bqCkmFVwXpOnm8W_q77zcFAf6l0"

supabase: Client = create_client("https://gmjnaofoppvjqtnrnrax.supabase.co", SUPABASE_API_KEY)

app = FastAPI()



@app.post("/sign_up")
async def sign_up_new_user(
    account_number: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
):
    try:
        auth_response = supabase.auth.sign_up({
        "email": email,
        "password": password
        })

        print(f"Response: {auth_response}")

        user_id = auth_response.user.id
        print(f"\n\nUser Id is: {user_id}\n\n")

        data = {
            "auth_id": user_id,
            "email": email,
            "phone_number": phone,
            "account_number": account_number
        }
        print(f"\n\nData: {data}\n\n")
        print(f"user_id is: {user_id}")
        return JSONResponse(content={"message": "User Entry Success", "user_id": user_id, "success": True}, status_code=200)        

    except Exception as e:
        print(f"The error in sign_up_new_user is: {e}")
        return JSONResponse(content={"message": "Error Creating New User", "success": False}, status_code=500)
    


@app.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        user_id = auth_response.user.id
        print(f"\n\nUser Id is: {user_id}\n\n")
        return JSONResponse(content={"message": "Login Success", "user_id": user_id, "success": True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Error Logging In: {e}", "success": False}, status_code=500)




@app.post("/users_b")
async def data_entry(
    account_number: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    country: str = Form(...),
    zip_code: str = Form(...),
    preferred_language: str = Form(...),
    risk_level: str = Form(...),
    savings_amount: float = Form(...),
    salary: float = Form(...),
    years_to_retirement: int = Form(...),
    employment_status: str = Form(...),
    marital_status: str = Form(...),
    dependents: int = Form(...),
    income_source: str = Form(...),
    occupation: str = Form(...),
    investment_preferences: str = Form(...),
    account_status: str = Form(...),
    debit_card_number: str = Form(...)
):
    try:

        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            user_id = auth_response.user.id
        except Exception as e:
            print(f"Login Failed: {e}")
            return JSONResponse(content={"message": "Failed while getting the auth_id itself", "success":False}, status_code=500)


        data = {
            "auth_id": user_id,
            "email": email,
            "phone_number": phone_number,
            # "account_number": account_number,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            # "date_of_birth": date_of_birth,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "zip_code": zip_code,
            # "registration_date": datetime.utcnow(),
            # "last_login": datetime.utcnow(),  # Assuming the user is logging in for the first time
            "is_active": True,
            "is_verified": False,
            "preferred_language": preferred_language,
            "risk_level": risk_level,
            "savings_amount": savings_amount,
            "salary": salary,
            "years_to_retirement": years_to_retirement,
            "employment_status": employment_status,
            "marital_status": marital_status,
            "dependents": dependents,
            "income_source": income_source,
            "occupation": occupation,
            "investment_preferences": investment_preferences,
            "account_status": account_status,
            "debit_card_number": debit_card_number
        }

        # Insert the user data into the 'users_b' table
        response = supabase.table("users_b").insert(data).execute()
        user_data = {
            "username": response['username']
        }
        print(f"\n\nResponse is:\n{response}\n\n")
        # print(f"\n\nResponse is:\n{response}\n\n")


        return JSONResponse(content={"message": "Added in Database at users_b table", "data": user_data, "success": True}, status_code=200)

    except Exception as e:
        print(f"\n\nError in data_entry is:\n{e}\n\n")
        return JSONResponse(content={"message": "Did not work adding", "success": False}, status_code=500)






# @app.post("/fetch_account_data")
# async def get_home_page_data(
#     user_id: str = Form(...)
# ):
#     try:
#         response = await get_user_data(user_id)
#     except Exception as e:
#         print(f"The error in get_home_page_data is: {e}")
#         return JSONResponse(content={"message": "Error Fetching Home Page data", "success": False}, status_code=500)







# @app.post("/chat_text")
# async def chat_text(
#     text_input: str = Form(...),
#     language: str = Form(...),
#     user_id: str = Form(...)
# ):
#     try:
#         text = text_input
#         english_text = await translation(language, "English", text)
#         eng_text = english_text['tranlated_content']
#         answer = await chatbot_response(eng_text, user_id)
#         answer_json = await translation("English", language, answer)
#         output = answer_json['translated_content']
#         if output:
#             print(f"The answer: {output}")
#             return JSONResponse(content={"message": "Got the answer", "output": output, "success": True}, status_code=200)
#         print(f"Output Content empty: {output}")
#         return JSONResponse(content={"message": "The output is empty", "success": False}, status_code=500)
#     except Exception as e:
#         print(f"The error in chat_text is: {e}")
#         return JSONResponse(content={"message": "Error Fetching Answer", "success": False}, status_code=500)
    




