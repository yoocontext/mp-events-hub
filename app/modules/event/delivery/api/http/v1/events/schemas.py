from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateEventInSchema(BaseModel):
    title: str
    scheduled_at: datetime
    description: str
    city: Optional[str] = None
    street: Optional[str] = None
    building_number: Optional[int] = None
    block: Optional[str] = None
    auditorium: Optional[str] = None


class CreateEventOutSchema(BaseModel):
    event_id: UUID


class UpdateEventOutSchema(BaseModel):
    event_id: UUID


class RegisterForEventOutSchema(BaseModel):
    user_id: UUID
    event_id: UUID


class GetEventOutSchema(BaseModel):
    events: list["EventSchema"]


class EventSchema(BaseModel):
    id: UUID
    title: str
    description: str
    created_by_fullname: str
    created_by_id: UUID
    scheduled_at: datetime
    image_id: UUID
    address: Optional["AddressSchema"]


class AddressSchema(BaseModel):
    city: str | None = None
    street: str | None = None
    building_number: int | None = None
    block: str | None = None
    auditorium: str | None = None
