from dataclasses import dataclass

from sqlalchemy import select, and_

from modules.event.domain.aggregate.event_registration import EventRegistration
from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.infra.dm.event import IEventDm
from modules.event.infra.dm.event_registration import IEventRegistrationDm
from modules.event.infra.dm.user import IUserDm
from modules.event.infra.mappers.event_registration import EventRegistrationMapper
from modules.event.infra.pg.models import EventRegistrationOrm, UserEventOrm, EventOrm
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class EventRegistrationAlchemyRepository(
    IEventRegistrationRepository,
    BaseAlchemyRepository,
):
    _user_dm: IUserDm
    _event_dm: IEventDm
    _event_registration_dm: IEventRegistrationDm
    _mapper: EventRegistrationMapper

    async def create(
        self,
        event_registration: EventRegistration,
    ) -> None:
        user_orm: UserEventOrm = await self._user_dm.get_by_id(
            _id=event_registration.user_id.value,
            events_created_load=False,
            registered_events_load=True,
        )
        event_orm: EventOrm = await self._event_dm.get_by_id(
            _id=event_registration.event_id.value,
        )

        user_orm.registered_events.append(event_orm)

    async def get_by_id(
        self,
        user_id: EntityIdValue,
        event_id: EntityIdValue,
    ) -> EventRegistration:
        event_registration_orm: EventRegistrationOrm = await (
            self._event_registration_dm.get_by_id(
                user_id=user_id.value,
                event_id=event_id.value,
            )
        )

        event_registration: EventRegistration = self._mapper.to_entity(
            event_registration_orm=event_registration_orm,
        )

        return event_registration

    async def delete(
        self,
        event_registration: EventRegistration,
    ) -> None:
        await self._event_registration_dm.delete(_id=event_registration.id.value)

    async def exists(
        self,
        user_id: EntityIdValue,
        event_id: EntityIdValue,
    ) -> bool:
        result = await self._session.execute(
            select(EventRegistrationOrm)
            .where(
                and_(
                    EventRegistrationOrm.user_uid == user_id.value,
                    EventRegistrationOrm.event_uid == event_id.value,
                )
            )
        )

        event_registration_orm: EventRegistrationOrm | None = result.scalar_one_or_none()

        if event_registration_orm:
            return True

        else:
            return False