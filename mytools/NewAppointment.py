import requests
import json
from pydantic import BaseModel, Field
from langchain_community.tools import BaseTool
from typing import Optional, Type
from datetime import datetime

def createNewAppointment(name: str, service: str, date: str, time: str):
    """
    Sends a webhook notification with the specified parameters.

    Parameters:
    - number (str): The number associated with the appointment.
    - name (str): The name associated with the appointment.
    - service (str): The service associated with the appointment.
    - date (str): The date associated with the appointment.
    - time (str): The time associated with the appointment.

    Returns:
    - response (requests.Response): The response object returned by the webhook request.
    """
    # Format date to dd-mm-yyyy if not already in that format
    try:
        formatted_date = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use dd-mm-yyyy.")
        return None

    # Format time to HH:MM if not already in that format
    try:
        formatted_time = datetime.strptime(time, "%H:%M").strftime("%H:%M")
    except ValueError:
        print("Invalid time format. Please use HH:MM.")
        return None

    # Create a dictionary containing the parameters
    payload = {
        "name": name,
        "service": service,
        "date": formatted_date,
        "time": formatted_time
    }

    webhook_url = "https://hook.eu2.make.com/3isaplviaow4trke9d3p9vddugtmbbcb"

    try:
        # Send POST request to the webhook URL with the payload
        response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise an error for unsuccessful responses
        return response
    except requests.exceptions.RequestException as e:
        print("Error sending webhook:", e)

class NewAppointmentInput(BaseModel):
    """Input for a new appointment."""

    name: str = Field(..., description="The name associated with the appointment.")
    service: str = Field(..., description="The service associated with the appointment. This has to be either Cornrows, Box Braids, Senegalese Twists, Goddess Braids, Feed-In Braids, Crochet Braids or Individual Braids.")
    date: str = Field(..., description="The date associated with the appointment. Use the format %d-%m-%Y.")
    time: str = Field(..., description="The time associated with the appointment. Use the format %H:%M.")

class NewAppointmentTool(BaseTool):
    name = "createNewAppointment"
    description = "Creates a new appointment"

    def _run(self, name: str, service: str, date: str, time: str):
        response = createNewAppointment(name, service, date, time)

        return response

    def _arun(self, name: str, service: str, date: str, time: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = NewAppointmentInput
