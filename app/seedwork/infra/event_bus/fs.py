import asyncio
from dataclasses import dataclass, asdict
from typing import TypeVar

from faststream.rabbit import RabbitBroker

from seedwork.domain.events.base import DomainEvent
from seedwork.application.interface.event_bus import IEventBus, QueueRmq
from seedwork.infra.event_bus.exceptions import QueueNotFoundException


DE = TypeVar("DE", bound=DomainEvent)


@dataclass
class FsEventBus(IEventBus):
    _broker: RabbitBroker
    _event_queue_map: dict[type[DomainEvent], QueueRmq]

    async def publish(self, events: list[DE]) -> None:
        tasks = []

        for event in events:
            queue: QueueRmq = self.__get_queue_by_event(event=event)
            task = self._broker.publish(
                message=asdict(event),
                queue=queue,
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

    def __get_queue_by_event(self, event: DomainEvent) -> QueueRmq:
        queue: QueueRmq | None = self._event_queue_map.get(type(event), None)

        if queue is None:
            raise QueueNotFoundException(event=event)

        return queue