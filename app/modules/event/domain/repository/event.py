from dataclasses import dataclass

from modules.event.domain.aggregate.event import Event
from seedwork.domain.event_store import IEventStore, EventTypeMap
from seedwork.domain.events.base import DomainEvent
from seedwork.domain.repository import BaseRepository
from seedwork.domain.value_objects.common.aggregate import (
    EntityIdValue,
    AggregateVersion,
)


@dataclass
class EventRepository(
    BaseRepository,
):
    _event_store: IEventStore

    async def save(self, event: Event) -> None:
        events: list[DomainEvent] = event.pull_events()
        current_agg_version: AggregateVersion = await (
            self._event_store.get_current_agg_version(aggregate_id=event.id)
        )

        if current_agg_version != event.loaded_version:
            ...
            # todo OptimisticLockException

        await self._event_store.save(events=events)

    async def load(
        self,
        aggregate_id: EntityIdValue,
        event_map: EventTypeMap,
    ) -> Event:
        events: list[DomainEvent] = await self._event_store.load(
            aggregate_id=aggregate_id,
            event_map=event_map,
        )

        return Event.rehydrate(events=events)
