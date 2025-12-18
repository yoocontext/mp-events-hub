from dataclasses import dataclass
from uuid import UUID

from modules.event.domain.aggregate.exceptions import CannotUnregisterOtherEvent
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


@dataclass
class EventRegistration(BaseAggregate):
    user_id: EntityIdValue
    event_id: EntityIdValue

    @classmethod
    def create(cls, user_id: UUID, event_id: UUID) -> "EventRegistration":
        return EventRegistration(
            user_id=EntityIdValue(user_id),
            event_id=EntityIdValue(event_id),
        )

    def delete(
        self,
        requester_user_id: EntityIdValue,
    ) -> None:
        if requester_user_id != self.user_id:
            raise CannotUnregisterOtherEvent()