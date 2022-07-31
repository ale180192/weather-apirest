import logging
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
    Date,
    Float,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import registry, relationship, composite
from sqlalchemy.sql.sqltypes import DateTime
from ...domain.models import City, Travel, TravelDatetimeRange, User, WeatherForecastDay

logger = logging.getLogger(__name__)
mapper_registry = registry()

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("email", String),
)

cities = Table(
    "cities",
    mapper_registry.metadata,
    Column("iso_code", String, primary_key=True),
    Column("name", String),
    Column("lon", String),
    Column("lat", String),
)

weather_forecast_days = Table(
    "weather_forecast_days",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("date", Date),
    Column("city_id", ForeignKey("cities.iso_code")),
    Column("max_temp", Float),
    Column("min_temp", Float),
    Column("avg_temp", Float),
    Column("daily_chance_of_rain", Integer),

    UniqueConstraint('city_id', 'date', name='ui_primarykey_citydate')
)

travels = Table(
    "travels",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("weather_forecast_origin_id", ForeignKey("weather_forecast_days.id")),
    Column("weather_forecast_destination_id", ForeignKey("weather_forecast_days.id")),
    Column("origin", String),
    Column("destination", String),
    Column("datetime_departure", DateTime),
    Column("datetime_arrival", DateTime)
)

def start_mappers():
    logger.info("Starting mappers")

    mapper_registry.map_imperatively(
        City, cities,
        properties={'weather_forecast_days': relationship(WeatherForecastDay, backref="cities")}
    )

    mapper_registry.map_imperatively(
        WeatherForecastDay, weather_forecast_days, properties={
            "city": relationship(City),
        }
    )

    mapper_registry.map_imperatively(
        Travel, travels, properties={
            "user": relationship(User),
            "weather_forecast_origin": relationship(WeatherForecastDay, foreign_keys=[travels.c.weather_forecast_origin_id]),
            "weather_forecast_destination": relationship(WeatherForecastDay, foreign_keys=[travels.c.weather_forecast_destination_id]),
            "datetime_range": composite(TravelDatetimeRange, travels.c.datetime_departure, travels.c.datetime_arrival)
            }
    )
    mapper_registry.map_imperatively(
        User,
        users,
        properties={'travels': relationship(Travel, backref="users")}
    )

