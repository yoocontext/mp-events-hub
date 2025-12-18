from dataclasses import dataclass

from modules.auth.domain.aggregate.user import User
from modules.auth.infra.pg.models.user import UserAuthOrm
from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.mapper import BaseMapper
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.user import NameValue, GroupNumberValue, EmailValue


@dataclass
class UserMapper(BaseMapper):
    @staticmethod
    def to_orm(user: User) -> UserAuthOrm:
        return UserAuthOrm(
            uid=user.id.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
            name=user.name.value,
            second_name=user.second_name.value,
            group_number=user.group_number.value,
            email=user.email.value,
            hash_password=user.hash_password,
            email_confirm=user.email_confirm,
        )

    @staticmethod
    def to_entity(user_orm: UserAuthOrm) -> User:
        return User(
            id=EntityIdValue(_value=user_orm.uid),
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at,
            name=NameValue(_value=user_orm.name),
            second_name=NameValue(_value=user_orm.second_name),
            group_number=GroupNumberValue(_value=user_orm.group_number),
            email=EmailValue(_value=user_orm.email),
            hash_password=user_orm.hash_password,
            role=RoleValue(user_orm.role.name),
            email_confirm=user_orm.email_confirm,
        )
