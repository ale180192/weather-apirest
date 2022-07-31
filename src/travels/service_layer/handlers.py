import logging
from typing import Callable
from uuid import uuid4

from dependency_injector.wiring import inject, Provide

from travels.adapters.weather_client import WeatherClient
from travels.container import Container
from travels.domain.models import Travel, TravelDatetimeRange
from travels.domain import events, commands

logger = logging.getLogger(__name__)

# Here all the use cases.

@inject
def create_travel(
    cmd: commands.CreateTravel,
    uow = Provide[Container.uow],
    weather_client: WeatherClient = Provide[Container.weather_client]
) -> Travel:
    logger.info("Command create_travel ...")
    with uow:
        datetime_range = TravelDatetimeRange(
            departure=cmd.date_departure,
            arrival=cmd.date_arrival
        )
        city_departure = uow.travels.get_city_by_isocode(iso_code=cmd.origin)
        city_destination = uow.travels.get_city_by_isocode(iso_code=cmd.destination)
        user = uow.travels.get_user_byid(cmd.user_id)

        weather_departure_data = weather_client.get_forecast_for_date(
            lat=city_departure.lat, lon=city_departure.lon, forecast_date=cmd.date_departure.date()
        )
        weather_destination_data = weather_client.get_forecast_for_date(
            lat=city_departure.lat, lon=city_departure.lon, forecast_date=cmd.date_departure.date()
        )
        weather_departure_data["id"] = uuid4().hex
        weather_destination_data["id"] = uuid4().hex
        weather_destination = uow.travels.get_or_create_weather_day(
            cmd.date_arrival,
            city_destination,
            defaults=weather_departure_data
        )
        weather_departure = uow.travels.get_or_create_weather_day(
            cmd.date_departure,
            city_departure,
            defaults=weather_destination_data
        )

        travel = Travel(
            id=cmd.id,
            user=user,
            origin=cmd.origin,
            destination=cmd.destination,
            datetime_range=datetime_range,
            weather_forecast_origin=weather_departure,
            weather_forecast_destination=weather_destination,
        )
        uow.travels.add(travel)
        travel.events.append(
            events.TravelCreated(travel.id, travel.origin)
        )
        uow.commit()
    return travel


@inject
def publish_travel_created(
    event: events.TravelCreated,
    publisher: Callable = Provide[Container.publisher]
):
    logger.info("publish to redis ...")
    publisher.publish("travel_created", event)


# TODO(alex): to do other microservice to counsume this TravelCreated event.
EVENTS_HANDLERS = {
    events.TravelCreated: [publish_travel_created,]
}

COMMAND_HANDLERS = {
    commands.CreateTravel: create_travel
}