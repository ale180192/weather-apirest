from dataclasses import dataclass
from datetime import datetime, date

class DateDepartureGreaterThanArrivalException(Exception):
    pass

class TravelDaysExceededException(Exception):
    pass

class City:

    def __init__(self, name: str, iso_code: str, lon: str, lat: str):
        self.name = name
        self.iso_code = iso_code
        self.lon = lon
        self.lat = lat


class WeatherForecastDay:
    max_temp: str
    def __init__(
        self,
        id: str,
        date: date,
        city: City,
        max_temp: float,
        min_temp: float,
        avg_temp: float,
        daily_chance_of_rain: int
    ):
        self.id = id
        self.date = date
        self.city = city
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.avg_temp = avg_temp
        self.daily_chance_of_rain = daily_chance_of_rain



class User:

    def __init__(self, id: str, email: str) -> None:
        self.id = id
        self.email = email


@dataclass(frozen=True)
class TravelDatetimeRange:
    departure: datetime
    arrival: datetime

    def __post_init__(self):
        if self.departure >= self.arrival:
            raise DateDepartureGreaterThanArrivalException()

    def __composite_values__(self):
        # method only used by the sqlalchemy ORM!!!
        return self.departure, self.arrival

class Travel:
    MAX_TRAVEL_DAYS = 8


    def __init__(
        self,
        id: str,
        user: User,
        origin: City,
        destination: City,
        datetime_range: TravelDatetimeRange,
        weather_forecast_origin: WeatherForecastDay,
        weather_forecast_destination: WeatherForecastDay,
    ) -> None:

        self.id = id
        self.user = user
        self.datetime_range = datetime_range
        self.origin = origin
        self.destination = destination
        self.weather_forecast_origin = weather_forecast_origin
        self.weather_forecast_destination = weather_forecast_destination
        self.events = []


