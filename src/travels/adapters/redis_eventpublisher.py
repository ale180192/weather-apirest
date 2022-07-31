import json
import logging
from dataclasses import asdict
import redis

from travels.domain import events
from travels.conf import conf

redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT, db=0)

logger = logging.getLogger(__name__)

class Publisher:

    def publish(self, channel, event: events.Event):
        logging.info("publishing: channel=%s, event=%s", channel, event)
        redis.publish(channel, json.dumps(asdict(event)))
