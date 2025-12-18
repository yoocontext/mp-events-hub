from modules.event.domain.aggregate.user import User
from modules.event.infra.pg.models import UserEventOrm
from seedwork.domain.mapper import BaseMapper
from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


class UserMapper(BaseMapper):
    @staticmethod
    def to_entity(user_orm: UserEventOrm) -> User:
        return User(
            id=EntityIdValue(user_orm.uid),
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at,
            role=RoleValue(user_orm.role.name),
        )

    @staticmethod
    def to_orm(user: User) -> UserEventOrm:
        return UserEventOrm(
            uid=user.id.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )