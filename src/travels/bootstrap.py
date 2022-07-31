import sys
from typing import Tuple

from travels.adapters.orm import schemas
from travels.service_layer.messagebus import MessageBus
from travels.service_layer import handlers
from .container import Container

modules = sys.modules[__name__]

def bootstrap(start_mappers=True) -> Tuple[Container, MessageBus]:
    if start_mappers:
        schemas.start_mappers()

    # dependency injection
    c = Container()
    c.wire(modules=[modules, "travels.service_layer.handlers"])
    bus = c.messagebus(handlers.EVENTS_HANDLERS, handlers.COMMAND_HANDLERS)
    return c, bus
