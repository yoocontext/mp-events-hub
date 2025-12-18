from abc import ABC, abstractmethod
from dataclasses import dataclass

from seedwork.infra.exception import InfraException


class EventStoreAlchemyException(
    InfraException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "EventStore alchemy exception"


@dataclass
class EventNotRegisteredException(EventStoreAlchemyException):
    event_name: str
    version: int

    @property
    def message(self) -> str:
        return f"Событие '{self.event_name}' с версией {self.version} не зарегистрировано."