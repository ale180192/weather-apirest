import logging
import logging.config
import json
import redis
from datetime import datetime
from travels.conf.conf import REDIS_PORT

from travels import bootstrap
from travels.domain import commands
from travels.conf import conf

log_conf = f"{conf.BASE_DIR}/conf/logging.conf"
logging.config.fileConfig(log_conf, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# TODO(alex): conf of environment
redis = redis.Redis(host=conf.REDIS_HOST, port=REDIS_PORT)


def main():
    logger.info("Redis pubsub starting")
    _, bus = bootstrap.bootstrap()
    pubsub = redis.pubsub(ignore_subscribe_messages=True)
    # create travel is also expose on the api
    pubsub.subscribe("create_travel")

    for m in pubsub.listen():
        handle_create_travel(m, bus)


def handle_create_travel(m, bus):
    logger.info("handling %s", m)
    data = json.loads(m["data"])
    date_departure = datetime.strptime(data["datetime_departure"], "%Y-%m-%dT%H:%M:%S")
    date_arrival = datetime.strptime(data["datetime_arrival"], "%Y-%m-%dT%H:%M:%S")
    cmd = commands.CreateTravel(
        id=data["id"],
        user_id=data["user_id"],
        origin=data["origin"],
        destination=data["destination"],
        date_departure=date_departure,
        date_arrival=date_arrival,
    )
    bus.handle(cmd)


if __name__ == "__main__":
    main()
