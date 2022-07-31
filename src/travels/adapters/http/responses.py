


from datetime import datetime
from pydantic import BaseModel

class TravelResponse(BaseModel):
    id: str
    origin: str
    destination: str
    datetime_departure: datetime
    datetime_arrival: datetime
    user_id: str
    # probability_of_rain: int

    class Config:
        orm_mode = True