import abc
from datetime import date

from sqlalchemy.orm import Query

from ..domain.models import (
    City,
    Travel,
    User,
    WeatherForecastDay,
)

class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Travel]

    def add(self, travel: Travel):
        self._add(travel)
        self.seen.add(travel)

    def get(self, sku) -> Travel:
        travel = self._get(sku)
        if travel:
            self.seen.add(travel)
        return travel

    @abc.abstractmethod
    def _add(self, product: Travel):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> Travel:
        raise NotImplementedError


class SqlTravelRepository(AbstractRepository):

    def __init__(self, session=None) -> None:
        super().__init__()
        self.session = session

    def _add(self, travel: Travel) -> Travel:
        self.session.add(travel)

    def _get(self, id: str) -> None:
        return None

    def get_city_by_isocode(self, iso_code: str) -> City:
        query: Query = self.session.query(City)
        city = query.get({"iso_code": iso_code})
        
        return city

    def get_or_create_weather_day(self, date, city, defaults=None) -> City:
        instance = self.session.query(WeatherForecastDay) \
            .filter_by(date=date.date(), city=city) \
            .first()
        if instance:
            return instance
        else:
            instance = WeatherForecastDay(date=date.date(), city=city, **defaults)
            self.session.add(instance)
            return instance

    def get_user_byid(self, user_id: str) -> User:
        query: Query = self.session.query(User)
        user = query.get(user_id)
        return user
 