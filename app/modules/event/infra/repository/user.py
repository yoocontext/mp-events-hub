from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from modules.event.infra.mappers.user import UserMapper
from modules.event.infra.pg.models import UserEventOrm
from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.user import IUserRepository
from seedwork.application.interface.dm.sql.roles import IRoleDm
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.infra.pg.excpetions import MissingRequiredFieldException
from seedwork.infra.pg.models import RoleOrm
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class UserAlchemyRepository(
    IUserRepository,
    BaseAlchemyRepository,
):
    _role_dm: IRoleDm
    _mapper: UserMapper

    async def get_by_id(self, required_id: EntityIdValue) -> User:
        result = await self._session.execute(
            select(UserEventOrm)
            .where(UserEventOrm.uid == required_id.value)
            .options(
                joinedload(UserEventOrm.role)
            )
        )

        user_orm: UserEventOrm | None = result.scalar_one_or_none()

        if user_orm:
            user: User = self._mapper.to_entity(user_orm)
            return user

        raise MissingRequiredFieldException(
            required_field="event_user.uid",
        )

    async def create(self, user: User) -> None:
        user_orm: UserEventOrm = self._mapper.to_orm(user)

        role: RoleOrm = await self._role_dm.get_by_name(role=user.role)

        user_orm.role = role

        self._session.add(user_orm)