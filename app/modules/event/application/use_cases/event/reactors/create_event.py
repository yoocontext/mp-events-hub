from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.application.interfaces.projection_services import IEventProjectionService
from modules.event.application.projections.event import EventProjection, AddressProjection
from seedwork.application.use_case import BaseUseCase


@dataclass
class CreateEventElasticCommand:
    id: UUID
    created_at: datetime
    created_by_user_id: UUID
    title: str
    scheduled_at: datetime
    description: str
    image_id: UUID
    city: str | None
    street: str | None
    building_number: int | None
    block: str | None
    auditorium: str | None


@dataclass
class CreateEventElasticUseCase(
    BaseUseCase[CreateEventElasticCommand, None]
):
    _event_projection_service: IEventProjectionService

    async def act(
        self,
        command: CreateEventElasticCommand,
    ) -> None:

        address: AddressProjection | None = None
        if command.city:
            address = AddressProjection(
                city=command.city,
                street=command.street,
                building_number=command.building_number,
                block=command.block if command.block else None,
                auditorium=command.auditorium if command.auditorium else None,
            )

        event_projection = EventProjection(
            id=command.id,
            title=command.title,
            description=command.description,
            created_by_fullname="", # todo сделать read model на юзера и экстрактить значения сюда
            created_by_id=command.created_by_user_id,
            scheduled_at=command.scheduled_at,
            image_id=command.image_id,
            address=address,
        )
        await self._event_projection_service.create(event=event_projection)