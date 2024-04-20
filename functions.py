from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()
import json

# Your Twilio API credentials
account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTHTOKEN"]

# Initialize Twilio client
client = Client(account_sid, auth_token)


def getMessageLog(otherNumber: str, twilioNumber: str=os.environ["TWILIO_NUMBER"]) -> dict:
    # Define the phone numbers between which you want to retrieve message logs

    # Retrieve sent messages
    sent_messages = client.messages.list(
        from_=twilioNumber,  # Filter messages sent from your Twilio number
        to=otherNumber  # Filter messages sent to the other number
    )

    # Retrieve received messages
    received_messages = client.messages.list(
        from_=otherNumber,  # Filter messages sent from the other number
        to=twilioNumber  # Filter messages sent to your Twilio number
    )

    # Combine sent and received messages
    all_messages = sent_messages + received_messages

    # Sort messages by date_sent
    all_messages.sort(key=lambda x: x.date_sent)

    # Create full log
    log: dict = {}
    for message in all_messages:
        log[message.sid] = {
            "From": message.from_,
            "To": message.to,
            "Body": message.body,
            "Date": message.date_sent,
            "Message SID": message.sid
            }
    return log

def getjson(file):
    with open(file) as db:
        return json.load(db)



