from dataclasses import dataclass
from datetime import datetime


class Command:
    pass

@dataclass
class CreateTravel(Command):
    user_id: str
    origin: str
    destination: str
    date_departure: datetime
    date_arrival: datetime
    id: str = None
