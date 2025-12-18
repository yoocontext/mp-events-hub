from dataclasses import dataclass

from modules.event.domain.value_objects.address import AddressValue
from modules.event.domain.value_objects.event import TitleValue, ScheduledAtValue, DescriptionValue
from modules.event.infra.pg.models.address import AddressOrm
from modules.event.infra.pg.models.event import EventOrm
from modules.event.domain.aggregate.event import Event
from modules.event.infra.mappers.address import AddressMapper
from seedwork.domain.mapper import BaseMapper
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.s3 import S3IdValue


@dataclass
class EventMapper(BaseMapper):
    _address_mapper: AddressMapper

    def to_orm(self, event: Event) -> EventOrm:
        address_orm: AddressOrm | None = None

        if event.address:
            address_orm = self._address_mapper.to_orm(address=event.address)

        return EventOrm(
            uid=event.id.value,
            created_at=event.created_at,
            updated_at=event.updated_at,
            title=event.title.value,
            description=event.description.value,
            image_uid=event.image_id.value,
            scheduled_at=event.scheduled_at.value,
            created_by_user_id=event.created_by_user_id.value,
            address=address_orm,
        )

    def to_entity(self, event_orm: EventOrm) -> Event:
        address_vo: AddressValue | None = None

        if event_orm.address:
            address_vo = self._address_mapper.to_value_object(
                address_orm=event_orm.address,
            )

        return Event(
            id=EntityIdValue(event_orm.uid),
            created_at=event_orm.created_at,
            updated_at=event_orm.updated_at,
            created_by_user_id=EntityIdValue(event_orm.created_by_user_id),
            title=TitleValue(event_orm.title),
            scheduled_at=ScheduledAtValue(event_orm.scheduled_at),
            address=address_vo,
            description=DescriptionValue(event_orm.description),
            image_id=S3IdValue(event_orm.image_uid),
        )