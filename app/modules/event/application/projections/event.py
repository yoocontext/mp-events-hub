from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from seedwork.domain.marker import EMPTY


@dataclass(
    frozen=True,
    slots=True,
)
class EventProjection:
    id: UUID
    title: str
    description: str
    created_by_fullname: str
    created_by_id: UUID
    scheduled_at: datetime
    image_id: UUID
    address: Optional["AddressProjection"]


@dataclass(
    frozen=True,
    slots=True,
)
class AddressProjection:
    city: str | None = None
    street: str | None = None
    building_number: int | None = None
    block: str | None = None
    auditorium: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class UpdateEventProjection:
    id: UUID
    title: str | None | EMPTY
    description: str | None | EMPTY
    created_by_fullname: str | None | EMPTY
    created_by_id: UUID | None | EMPTY
    scheduled_at: datetime | None | EMPTY
    image_id: UUID | None | EMPTY
    address: Optional["UpdateAddressProjection"] | EMPTY


@dataclass(
    frozen=True,
    slots=True,
)
class UpdateAddressProjection:
    city: str | None | EMPTY
    street: str | None | EMPTY
    building_number: int | None | EMPTY
    block: str | None | EMPTY
    auditorium: str | None | EMPTY