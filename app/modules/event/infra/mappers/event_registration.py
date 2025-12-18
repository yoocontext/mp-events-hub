from modules.event.domain.aggregate.event_registration import EventRegistration
from modules.event.infra.pg.models import EventRegistrationOrm
from seedwork.domain.mapper import BaseMapper
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


class EventRegistrationMapper(BaseMapper):
    @staticmethod
    def to_entity(
        event_registration_orm: EventRegistrationOrm,
    ) -> EventRegistration:
        return EventRegistration(
            id=EntityIdValue(event_registration_orm.uid),
            created_at=event_registration_orm.created_at,
            updated_at=event_registration_orm.updated_at,
            user_id=EntityIdValue(event_registration_orm.user_uid),
            event_id=EntityIdValue(event_registration_orm.event_uid),
        )