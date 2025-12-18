from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.exceptions import UserRoleNotAllowedException
from seedwork.domain.value_objects.exceptions import RoleValueException
from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


@dataclass
class User(BaseAggregate):
    role: RoleValue

    @classmethod
    def create(
        cls,
        _id: UUID,
        role: str,
    ) -> "User":
        try:
            role_vo = RoleValue(role)

        except ValueError:
            raise RoleValueException(value=role)

        return User(
            id=EntityIdValue(_id),
            role=role_vo,
        )

    def create_event(
        self,
        title: str,
        scheduled_at: datetime,
        description: str,
        image_id: UUID,
        city: str,
        street: str,
        building_number: int,
        block: str | None,
        auditorium: str | None,
    ) -> Event:
        if self.role not in (RoleValue.ORGANIZER, RoleValue.ADMIN):
            raise UserRoleNotAllowedException(self.role.value)

        event = Event()
        event.create()
        return event