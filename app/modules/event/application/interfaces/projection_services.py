from abc import ABC, abstractmethod
from uuid import UUID

from modules.event.application.projections.event import EventProjection
from seedwork.domain.value_objects.paginator import (
    LimitPaginatorValue,
    OffsetPaginatorValue,
)


class IEventProjectionService(ABC):
    @abstractmethod
    async def search(
        self,
        query: str | None = None,
        event_id: UUID | None = None,
        created_by_user_id: UUID | None = None,
        limit: LimitPaginatorValue = LimitPaginatorValue(25),
        offset: OffsetPaginatorValue = OffsetPaginatorValue(0),
    ) -> list[EventProjection]:
        ...

    @abstractmethod
    async def create(self, event: EventProjection) -> None:
        ...
