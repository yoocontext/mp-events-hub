from abc import ABC, abstractmethod

from seedwork.domain.events.base import DomainEvent
from seedwork.domain.value_objects.common.aggregate import EntityIdValue, AggregateVersion
from seedwork.infra.event_store.exception import EventNotRegisteredException


class IEventStore(ABC):
    @abstractmethod
    async def save(
        self,
        events: list[DomainEvent],
    ) -> None:
        ...

    @abstractmethod
    async def load(
        self,
        aggregate_id: EntityIdValue,
        event_map: "EventTypeMap",
    ) -> list[DomainEvent]:
        ...

    @abstractmethod
    async def get_current_agg_version(
        self,
        aggregate_id: EntityIdValue,
    ) -> AggregateVersion:
        ...

class EventTypeMap:
    def __init__(self):
        self._map: dict[tuple[str, int], type[DomainEvent]] = {}

    def register(
        self,
        event_name: str,
        version: int,
        event_class: type[DomainEvent],
    ):
        key = (event_name, version)
        self._map[key] = event_class

    def get(
        self,
        event_type: str,
        version: int,
    ) -> type[DomainEvent]:
        ev_type: type[DomainEvent] | None = self._map.get((event_type, version), None)

        if ev_type:
            return ev_type

        raise EventNotRegisteredException(
            event_name=event_type,
            version=version,
        )

    def __contains__(self, item: tuple[str, int]):
        return item in self._map

    def __repr__(self):
        return f"EventTypeMap({self._map})"
