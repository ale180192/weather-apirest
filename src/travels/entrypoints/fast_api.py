import logging
import os
from uuid import uuid4
from fastapi import FastAPI

from travels import bootstrap
from travels.adapters.http import requests
from travels.domain import commands


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig(f"{BASE_DIR}/conf/logging.conf", disable_existing_loggers=False)
app = FastAPI()
container, bus = bootstrap.bootstrap()

logger = logging.getLogger(__name__)

@app.post("/travels")
def create_travel(travel_request: requests.TravelRequest, ):
    logger.info("create travel endpoint call ...")
    cmd = commands.CreateTravel(
        id=uuid4().hex,
        user_id=travel_request.user_id,
        origin=travel_request.origin,
        destination=travel_request.destination,
        date_departure=travel_request.datetime_departure,
        date_arrival=travel_request.datetime_arrival,
    )

    bus.handle(cmd)
    return {"id": cmd.id}
