from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from seedwork.domain.events.base import DomainEvent
from seedwork.domain.marker import EMPTY


@dataclass(
    frozen=True,
    slots=True,
)
class CreateEventEvent(DomainEvent):
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


@dataclass(
    frozen=True,
    slots=True,
)
class UpdateEventEvent(DomainEvent):
    created_at: datetime | None | EMPTY = EMPTY
    created_by_user_id: UUID | None | EMPTY = EMPTY
    title: str | None | EMPTY = EMPTY
    scheduled_at: datetime | None | EMPTY = EMPTY
    description: str | None | EMPTY = EMPTY
    image_id: UUID | None | EMPTY = EMPTY
    city: str | None | EMPTY = EMPTY
    street: str | None | EMPTY = EMPTY
    building_number: int | None | EMPTY = EMPTY
    block: str | None | EMPTY = EMPTY
    auditorium: str | None | EMPTY = EMPTY


@dataclass(
    frozen=True,
    slots=True,
)
class DeleteEventEvent(DomainEvent):
    d_event_id: UUID