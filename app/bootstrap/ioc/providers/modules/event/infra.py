from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch

from modules.event.application.interfaces.projection_services import IEventProjectionService
from modules.event.domain.repository.event import IEventRepository
from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.domain.repository.user import IUserRepository
from modules.event.infra.dm.event import IEventDm, EventAlchemyDm
from modules.event.infra.dm.event_registration import IEventRegistrationDm, EventRegistrationAlchemyDm
from modules.event.infra.dm.user import IUserDm, UserAlchemyDm
from modules.event.infra.elastic.projection_services.event import EventProjectionElcService
from modules.event.infra.mappers.address import AddressMapper, BuildingMapper
from modules.event.infra.mappers.event import EventMapper
from modules.event.infra.mappers.event_registration import EventRegistrationMapper
from modules.event.infra.mappers.user import UserMapper
from modules.event.infra.repository.event import EventAlchemyRepository
from modules.event.infra.repository.event_registration import EventRegistrationAlchemyRepository
from modules.event.infra.repository.user import UserAlchemyRepository
from seedwork.application.interface.dm.sql.roles import IRoleDm


class DmEventProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
    ) -> IUserDm:
        return UserAlchemyDm(_session=session)

    @provide
    def event(
        self,
        session: AsyncSession,
    ) -> IEventDm:
        return EventAlchemyDm(_session=session)

    @provide
    def event_registration(
        self,
        session: AsyncSession,
    ) -> IEventRegistrationDm:
        return EventRegistrationAlchemyDm(_session=session)


class RepositoryEventProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
        role_dm: IRoleDm,
        mapper: UserMapper,
    ) -> IUserRepository:
        return UserAlchemyRepository(
            _session=session,
            _role_dm=role_dm,
            _mapper=mapper,
        )

    @provide
    def event(
        self,
        session: AsyncSession,
        event_mapper: EventMapper,
        address_mapper: AddressMapper,
        event_dm: IEventDm,
        user_dm: IUserDm,
    ) -> IEventRepository:
        return EventAlchemyRepository(
            _session=session,
            _event_mapper=event_mapper,
            _address_mapper=address_mapper,
            _event_dm=event_dm,
            _user_dm=user_dm,
        )

    @provide
    def event_registration(
        self,
        user_dm: IUserDm,
        event_dm: IEventDm,
        event_registration_dm: IEventRegistrationDm,
        mapper: EventRegistrationMapper,
        session: AsyncSession,
    ) -> IEventRegistrationRepository:
        return EventRegistrationAlchemyRepository(
            _user_dm=user_dm,
            _event_dm=event_dm,
            _event_registration_dm=event_registration_dm,
            _mapper=mapper,
            _session=session,
        )


class MapperEventProvider(Provider):
    scope = Scope.APP

    @provide
    def user(self) -> UserMapper:
        return UserMapper()

    @provide
    def event(
        self,
        address_mapper: AddressMapper,
    ) -> EventMapper:
        return EventMapper(
            _address_mapper=address_mapper,
        )

    @provide
    def address(
        self,
        building_mapper: BuildingMapper,
    ) -> AddressMapper:
        return AddressMapper(
            _building_mapper=building_mapper,
        )

    @provide
    def building(self) -> BuildingMapper:
        return BuildingMapper()

    @provide
    def event_registration(self) -> EventRegistrationMapper:
        return EventRegistrationMapper()


class EventProjectionProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def event(
        self,
        elastic: AsyncElasticsearch,
    ) -> IEventProjectionService:
        return EventProjectionElcService(
            _elc=elastic,
        )