# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
import abc
from sqlalchemy.orm.session import Session

from travels.adapters.orm.db_conf import get_sql_session
from travels.adapters.repositories import SqlTravelRepository, AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    travels: AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for travel in self.travels.seen:
            while travel.events:
                yield travel.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = get_sql_session()


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory
        self.travels = SqlTravelRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
