

from dataclasses import dataclass


class Event:
    pass


@dataclass
class TravelCreated(Event):
    id: str
    origin: str