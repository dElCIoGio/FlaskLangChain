import requests
import json
from pydantic import BaseModel, Field
from langchain_community.tools import BaseTool
from typing import Optional, Type

def notifyStaff(message: str):
    """
    Sends a webhook notification to a specified URL with a given message.

    Parameters:
    - webhook_url (str): The URL of the webhook to send the notification to.
    - message (str): The message to be sent in the webhook.

    Returns:
    - response (requests.Response): The response object returned by the webhook request.
    """
    # Create a dictionary containing the message
    payload = {"content": message}
    webhook_url = "https://hook.eu2.make.com/dwlei4zgbzfqbs98n1fw5fvvstnagngx"
    try:
        # Send POST request to the webhook URL with the message payload
        response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise an error for unsuccessful responses
        return response
    except requests.exceptions.RequestException as e:
        print("Error sending webhook:", e)


class NotifyStaffInput(BaseModel):
    """Input for staff notification."""

    message: str = Field(..., description="Message to be sent to the staff")

class NotifyStaffTool(BaseTool):
    name = "notifyStaff"
    description = "Sends a message notification to a TeeBraids staff."

    def _run(self, message: str):
        send_message = notifyStaff(message)

        return send_message

    def _arun(self, message: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = NotifyStaffInput