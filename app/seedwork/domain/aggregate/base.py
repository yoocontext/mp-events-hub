from abc import ABC, abstractmethod
from copy import copy
from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from seedwork.domain.entities import TimestampEntity
from seedwork.domain.events.base import DomainEvent
from seedwork.domain.value_objects.common.aggregate import (
    EntityIdValue,
    AggregateVersion,
)


@dataclass(
    kw_only=True,
    slots=True,
    init=False,
)
class BaseAggregate(
    TimestampEntity,
    ABC,
):
    _loaded_version: AggregateVersion = field(default=AggregateVersion(0))
    _version: AggregateVersion = field(default=AggregateVersion(0))
    _events: list[DomainEvent] = field(default_factory=list)

    def register_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        registered_events = copy(self._events)

        self._events.clear()

        return registered_events

    @classmethod
    def rehydrate(cls, events: list[DomainEvent]) -> "BaseAggregate":
        agg = cls.__new__(cls)
        super(cls, agg).__init__()

        events.sort(key=lambda x: x.version)
        agg._events = []

        for event in events:
            agg._when(event)

        event_with_max_version: DomainEvent = max(events, key=lambda e: e.version)
        max_version: int = event_with_max_version.version

        agg._loaded_version = AggregateVersion(max_version)
        agg._version = AggregateVersion(max_version)

        return agg

    def _apply(self, event: DomainEvent) -> None:
        self._events.append(event)
        self._when(event)
        self._bump_version()

    @abstractmethod
    def _when(self, event: DomainEvent) -> None:
        ...

    def _set_id(self, _id: UUID) -> None:
        _id = EntityIdValue(_id)
        self.id = _id

    def _set_version(self, version: int) -> None:
        _version = AggregateVersion(version)
        self._version = _version

    def _bump_version(self) -> None:
        new_version = AggregateVersion(self._version.value + 1)
        self._version = new_version

    @property
    def loaded_version(self) -> AggregateVersion:
        return self._loaded_version