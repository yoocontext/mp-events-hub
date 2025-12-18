from abc import ABC, abstractmethod
from typing import TypeVar

from seedwork.domain.events.base import DomainEvent


QueueRmq = TypeVar("QueueRmq", bound=str)


class IEventBus(ABC):
    @abstractmethod
    async def publish(
        self,
        events: list[DomainEvent],
    ) -> None:
        ...