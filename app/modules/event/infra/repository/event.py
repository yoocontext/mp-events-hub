from dataclasses import dataclass

from sqlalchemy.inspection import inspect

from modules.event.infra.dm.event import IEventDm
from modules.event.infra.dm.user import IUserDm
from modules.event.infra.mappers.address import AddressMapper
from modules.event.infra.pg.models import UserEventOrm, AddressOrm
from modules.event.infra.pg.models.event import EventOrm
from modules.event.domain.aggregate.event import Event
from modules.event.domain.repository.event import EventRepository
from modules.event.infra.mappers.event import EventMapper
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.infra.pg.models import BaseOrm
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class EventAlchemyRepository(
    EventRepository,
    BaseAlchemyRepository,
):
    _event_mapper: EventMapper
    _address_mapper: AddressMapper
    _event_dm: IEventDm
    _user_dm: IUserDm

    async def create(self, event: Event) -> None:
        event_orm: EventOrm = self._event_mapper.to_orm(event)
        user_orm: UserEventOrm = await self._user_dm.get_by_id(
            _id=event.created_by_user_id.value,
            events_created_load=False,
            registered_events_load=False,
        )

        event_orm.created_by_user = user_orm

        self._session.add(event_orm)

    async def get_by_id(self, _id: EntityIdValue) -> Event:
        event_orm: EventOrm = await self._event_dm.get_by_id(_id=_id.value)

        event: Event = self._event_mapper.to_entity(event_orm=event_orm)

        return event

    async def delete(self, _id: EntityIdValue) -> None:
        await self._event_dm.delete(_id=_id.value)

    async def update(self, event: Event) -> Event:
        event_orm: EventOrm = await self._event_dm.get_by_id(_id=event.id.value)

        new_data: EventOrm = self._event_mapper.to_orm(event)

        self._copy_orm_fields(source=new_data, target=event_orm)

        if event.address:
            address_orm: AddressOrm = self._address_mapper.to_orm(event.address)
            event_orm.address = address_orm

        new_event: Event = self._event_mapper.to_entity(event_orm)

        return new_event

    @staticmethod
    def _copy_orm_fields(source: BaseOrm, target: BaseOrm) -> None:
        mapper = inspect(EventOrm)

        attrs = list(mapper.column_attrs.values())

        for attr in attrs:
            name: str = attr.key

            if name in ("uid", "created_at",):
                continue

            setattr(target, name, getattr(source, name))
