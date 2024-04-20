import datetime
import requests
import json
from pydantic import BaseModel, Field
from langchain_community.tools import BaseTool
from typing import Optional, Type
import pytz


def get_current_date_and_time():
    london_tz = pytz.timezone('Europe/London')
    current_date_time = datetime.datetime.now(tz=london_tz)
    return current_date_time.strftime("(%A) %d-%m-%Y %H:%M:%S %Z")

class GetDateTimeInput(BaseModel):
    """Input for date and time."""

class GetDateTimeTool(BaseTool):
    name = "get_current_date_and_time"
    description = "Get current day and time (London) in the following format: (%A) %d-%m-%Y %H:%M:%S"

    def _run(self):
        getDateTime = get_current_date_and_time()

        return getDateTime

    def _arun(self):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetDateTimeInput

