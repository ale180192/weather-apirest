from datetime import datetime
from pydantic import BaseModel


class TravelRequest(BaseModel):
    origin: str
    destination: str
    datetime_departure: datetime
    datetime_arrival: datetime
    user_id: str