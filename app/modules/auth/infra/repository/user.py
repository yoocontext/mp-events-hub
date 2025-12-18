from dataclasses import dataclass

from sqlalchemy import select, update, exists, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.inspection import inspect

from seedwork.infra.pg.excpetions import MissingRequiredFieldException
from seedwork.infra.pg.models import RoleOrm
from seedwork.application.interface.dm.sql.roles import IRoleDm
from modules.auth.application.interface.dm.sql.user import IUserDm
from modules.auth.application.mappers.user import UserMapper
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.infra.pg.models.user import UserAuthOrm
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.user import (
    EmailValue,
    NameValue,
    GroupNumberValue,
)
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class UserAlchemyRepository(
    IUserRepository,
    BaseAlchemyRepository,
):
    _mapper: UserMapper
    _role_dm: IRoleDm
    _user_dm: IUserDm

    async def create(self, user: User) -> None:
        role_orm: RoleOrm = await (
            self._role_dm.get_by_name(role=user.role)
        )

        user_orm: UserAuthOrm = self._mapper.to_orm(user=user)
        user_orm.role_uid = role_orm.uid

        self._session.add(user_orm)

    async def update(self, user: User) -> User:
        user_orm: UserAuthOrm | None = await (
            self._user_dm.get_by_uid(uid=user.id.value, role_load=False)
        )

        if user_orm is None:
            raise MissingRequiredFieldException(
                required_field="user.id",
            )

        new_data: UserAuthOrm = self._mapper.to_orm(user)

        self._copy_orm_fields(source=new_data, target=user_orm)

        role_orm = await self._role_dm.get_by_name(role=user.role)

        user_orm.role_uid = role_orm.uid

        new_user: User = self._mapper.to_entity(user_orm=user_orm)

        return new_user

    async def is_email_taken(self, email: EmailValue) -> bool:
        result = await self._session.execute(
            select(
                exists()
                .where(
                    and_(
                        UserAuthOrm.email == email.value,
                        UserAuthOrm.email_confirm.is_(True),
                    )
                )
            )
        )
        return result.scalar()

    async def is_user_duplicate(
        self,
        name: NameValue,
        second_name: NameValue,
        group_number: GroupNumberValue,
    ) -> bool:
        result = await self._session.execute(
            select(
                exists()
                .where(
                    and_(
                        UserAuthOrm.name == name.value,
                        UserAuthOrm.second_name == second_name.value,
                        UserAuthOrm.group_number == group_number.value,
                        UserAuthOrm.email_confirm.is_(True),
                    )
                )
            )
        )
        return result.scalar()

    async def find_by_id(
        self,
        required_id: EntityIdValue,
    ) -> User | None:
        result = await self._session.execute(
            select(UserAuthOrm)
            .where(UserAuthOrm.uid == required_id.value)
            .options(
                joinedload(UserAuthOrm.role)
            )
        )

        user_orm: UserAuthOrm | None = result.scalar_one_or_none()

        if user_orm:
            user: User = self._mapper.to_entity(user_orm)
            return user

        else:
            return None

    async def find_by_email(
        self,
        email: EmailValue,
    ) -> User | None:
        result = await self._session.execute(
            select(UserAuthOrm)
            .where(
                and_(
                    UserAuthOrm.email == email.value,
                    UserAuthOrm.email_confirm.is_(True),
                )
            )
            .options(
                joinedload(UserAuthOrm.role)
            )
        )

        user_orm: UserAuthOrm | None = result.scalar_one_or_none()

        if user_orm:
            user: User = self._mapper.to_entity(user_orm)
            return user

        else:
            return None

    async def confirm_user(
        self,
        email: EmailValue,
    ) -> None:
        await self._session.execute(
            update(UserAuthOrm)
            .where(UserAuthOrm.email == email.value)
            .values(email_confirm=True)
        )

    @staticmethod
    def _copy_orm_fields(source: UserAuthOrm, target: UserAuthOrm) -> None:
        mapper = inspect(UserAuthOrm)

        attrs = list(mapper.column_attrs.values())

        for attr in attrs:
            name: str = attr.key

            if name in ("id", "uid", "role", "role_id", "created_at"):
                continue

            setattr(target, name, getattr(source, name))
