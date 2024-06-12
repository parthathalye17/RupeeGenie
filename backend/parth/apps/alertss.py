from twilio.rest import Client
from backend.mihiresh.bhashini import translation
import os
from dotenv import load_dotenv
load_dotenv()
account_sid = os.getenv("TWILIO_SID") 
auth_token = os.getenv("TWILLIO_KEY")
client = Client(account_sid, auth_token)

async def twilio_message(reply):
    message = client.messages.create(
        from_='+16506459305',
        body=reply,
        to='+919987117266')
    print(message.sid)
    
async def alert_message(risk,transaction,approval,language,phone_number,amount):
    try:
        if risk == 1:
            message = "Alert! Potential fraundlent transaction"
            trans_message = await translation("English", language, message)
            print(trans_message['translated_content'])
        if transaction:
            message = f"₹.{amount} was debitted from your account to {phone_number}."
            trans_message = await translation("English", language, message)
            print(trans_message['translated_content'])
        if approval == True:
            message = f"Your loan application has been sent."
            trans_message = await translation("English", language, message)
            print(trans_message['translated_content'])
    except Exception as e:
        print(f"Error: {str(e)}")
        return { "text": "Error processing alert message text", "success": False}
        
        
