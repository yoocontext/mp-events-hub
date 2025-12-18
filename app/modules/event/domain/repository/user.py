from abc import ABC, abstractmethod

from modules.event.domain.aggregate.user import User
from seedwork.domain.repository import BaseRepository
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


class IUserRepository(
    BaseRepository,
    ABC,
):
    @abstractmethod
    async def get_by_id(self, required_id: EntityIdValue) -> User:
        ...

    @abstractmethod
    async def create(self, user: User) -> None:
        ...