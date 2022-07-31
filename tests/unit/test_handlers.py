# pylint: disable=no-self-use
from datetime import datetime, timedelta
import sys

from dependency_injector import containers, providers
from uuid import uuid4
from travels.adapters.weather_client import WeatherClient
from travels.service_layer.messagebus import MessageBus
from travels.domain.models import User

from travels.adapters.repositories import AbstractRepository
from travels.domain.models import WeatherForecastDay, City, User
from travels.service_layer.unit_of_work import AbstractUnitOfWork
from travels.service_layer import handlers
from travels.bootstrap import bootstrap
from travels.domain import commands
from travels.adapters.redis_eventpublisher import Publisher



class FakeRepository(AbstractRepository):
    def __init__(self, cities=[], travels=[], users=[]):
        super().__init__()
        self._travels = travels
        self._cities = cities
        self._users = users
        self._weather_forecast_days = []

    def _add(self, travel):
        self._travels.append(travel)

    def get_city_by_isocode(self, iso_code):
        return next((c for c in self._cities if c.iso_code == iso_code), None)
    
    def get_user_byid(self, user_id: str) -> User:
        return next(
            (u for u in self._users if u.id == user_id),
            None
        )

    def get_or_create_weather_day(self, date, city, defaults=None):
        instance =  next(
            (w for w in self._weather_forecast_days \
                if (w.city.iso_code == city.iso_code) and (w.date == date)),
            WeatherForecastDay(
                date=date,
                city=city,
                **defaults
            ),
        )
        self._weather_forecast_days.append(instance)
        return instance

    def _get(self, id: str) -> None:
        return None

class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, travels=None):
        self.travels = travels
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass

class OverridingContainer(containers.DeclarativeContainer):

    travel_repository = providers.Singleton(
        FakeRepository
    )
    uow = providers.Singleton(
        FakeUnitOfWork,
        travels=travel_repository
    )
    publisher = providers.Singleton(
        Publisher
    )
    messagebus = providers.Factory(
        MessageBus,
        uow=uow
    )


class TestCreateTravel:

    def test_create_batch_happy_path(self):
        overriden_container = OverridingContainer()
        today = datetime.today()
        tomorrow = today + timedelta(days=2)
        cmd = commands.CreateTravel(
            id=uuid4().hex,
            user_id="user_id",
            origin="cdmx",
            destination="cancun",
            date_departure=today,
            date_arrival=tomorrow,
        )
        cities = [City(name="cdmx", iso_code="cdmx", lon="19.9", lat="20.8"), City(name="cancun", iso_code="cancun", lon="19.9", lat="20.8")]
        buss: MessageBus = overriden_container.messagebus(
                event_handlers=handlers.EVENTS_HANDLERS,
                command_handlers=handlers.COMMAND_HANDLERS,
                uow__travels__cities=cities
        )
        handlers.create_travel(cmd=cmd, uow=buss.uow, weather_client=WeatherClient())
        assert buss.uow.committed
