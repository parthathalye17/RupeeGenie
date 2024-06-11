from fastapi import FastAPI,File,UploadFile,Form, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
import json
from bhashini import text_to_speech, transcribe, translation
from chat_bot import chatbot_response

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

        # if auth_response.status_code != 200:
        #     raise HTTPException(status_code=auth_response.status_code, detail=auth_response.json())
        
        user_id = auth_response.json()['user']['id']

        data = {
            "id": user_id,
            "email": email,
            "phone": phone,
            "account_number": account_number
        }

        db_response = supabase.table('users').insert(data).execute()

        if db_response.status_code != 200:
            raise HTTPException(status_code=db_response.status_code, detail=db_response.json())

        print(f"user_id is: {user_id}")
        return JSONResponse(content={"message": "User Entry Success", "user_id": user_id, "success": True}, status_code=200)        

    except Exception as e:
        print(f"The error in sign_up_new_user is: {e}")
        return JSONResponse(content={"message": "Error Creating New User", "success": False}, status_code=500)
    



# @app.post("/fetch_account_data")
# async def get_home_page_data(
#     user_id: str = Form(...)
# ):
#     try:
#         response = await get_user_data(user_id)
#     except Exception as e:
#         print(f"The error in get_home_page_data is: {e}")
#         return JSONResponse(content={"message": "Error Fetching Home Page data", "success": False}, status_code=500)







@app.post("/chat_text")
async def chat_text(
    text_input: str = Form(...),
    language: str = Form(...),
    user_id: str = Form(...)
):
    try:
        text = text_input
        english_text = await translation(language, "English", text)
        eng_text = english_text['tranlated_content']
        answer = await chatbot_response(eng_text, user_id)
        answer_json = await translation("English", language, answer)
        output = answer_json['translated_content']
        if output:
            print(f"The answer: {output}")
            return JSONResponse(content={"message": "Got the answer", "output": output, "success": True}, status_code=200)
        print(f"Output Content empty: {output}")
        return JSONResponse(content={"message": "The output is empty", "success": False}, status_code=500)
    except Exception as e:
        print(f"The error in chat_text is: {e}")
        return JSONResponse(content={"message": "Error Fetching Answer", "success": False}, status_code=500)
    




