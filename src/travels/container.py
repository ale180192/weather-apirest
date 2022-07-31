import requests

from dependency_injector import containers, providers

from travels.adapters.weather_client import WeatherClient
from travels.adapters.orm import db_conf
from travels.adapters.repositories import SqlTravelRepository
from travels.service_layer.messagebus import MessageBus
from travels.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from travels.adapters.redis_eventpublisher import Publisher

session = db_conf.get_sql_session()


class Container(containers.DeclarativeContainer):
    
    session_single = providers.Singleton(session)
    travel_repository = providers.Singleton(
        SqlTravelRepository,
        session=session_single,
    )
    uow = providers.Singleton(
        SqlAlchemyUnitOfWork,
        session_factory=session_single
    )
    publisher = providers.Singleton(
        Publisher
    )
    messagebus = providers.Factory(
        MessageBus,
        uow=uow
    )
    weather_client = providers.Factory(
        WeatherClient,
    )
