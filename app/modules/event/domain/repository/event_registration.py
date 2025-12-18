from abc import ABC, abstractmethod

from modules.event.domain.aggregate.event_registration import EventRegistration
from seedwork.domain.repository import BaseRepository
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


class IEventRegistrationRepository(
    BaseRepository,
    ABC,
):
    @abstractmethod
    async def create(
        self,
        event_registration: EventRegistration,
    ) -> None:
        ...

    @abstractmethod
    async def get_by_id(
        self,
        user_id: EntityIdValue,
        event_id: EntityIdValue,
    ) -> EventRegistration:
        ...

    @abstractmethod
    async def delete(
        self,
        event_registration: EventRegistration,
    ) -> None:
        ...

    @abstractmethod
    async def exists(
        self,
        user_id: EntityIdValue,
        event_id: EntityIdValue,
    ) -> bool:
        ...
