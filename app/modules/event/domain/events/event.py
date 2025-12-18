from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from seedwork.domain.events.base import DomainEvent


@dataclass(frozen=True)
class CreateEventEvent(DomainEvent):
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
