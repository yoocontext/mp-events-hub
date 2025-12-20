from dataclasses import dataclass
from uuid import UUID

from modules.event.application.interfaces.projection_services import (
    IEventProjectionService,
)
from modules.event.application.projections.event import EventProjection
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.paginator import (
    LimitPaginatorValue,
    OffsetPaginatorValue,
)


@dataclass
class GetEventProjectionCommand:
    query: str | None
    event_id: UUID | None
    created_by_user_id: UUID | None
    limit: int
    offset: int


@dataclass
class GetEventProjectionUseCase(
    BaseUseCase[GetEventProjectionCommand, list[EventProjection]],
):
    _event_query_service: IEventProjectionService

    async def act(
        self,
        command: GetEventProjectionCommand,
    ) -> list[EventProjection]:

        limit = LimitPaginatorValue(command.limit)
        offset = OffsetPaginatorValue(command.offset)

        event_projections: list[EventProjection] = await (
            self._event_query_service.search(
                query=command.query,
                event_id=command.event_id,
                created_by_user_id=command.created_by_user_id,
                limit=limit,
                offset=offset,
            )
        )

        return event_projections
