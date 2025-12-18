from abc import ABC, abstractmethod
from datetime import timedelta

from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.user import EmailValue
from seedwork.infra.dm.base import BaseDataMapper


class IUserKvDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def save_confirm_code_by_id(
        self,
        user_id: EntityIdValue,
        confirm_code: ConfirmCodeValue,
        ttl: timedelta,
    ) -> None:
        ...

    @abstractmethod
    async def get_confirm_code_by_id(
        self,
        user_id: EntityIdValue,
    ) -> str | None:
        ...

    @abstractmethod
    async def save_confirm_code_by_email(
        self,
        email: EmailValue,
        confirm_code: ConfirmCodeValue,
        ttl: timedelta,
    ) -> None:
        ...

    @abstractmethod
    async def get_confirm_code_by_email(
        self,
        email: EmailValue,
    ) -> str | None:
        ...

    @abstractmethod
    async def save_password_by_email(
        self,
        email: EmailValue,
        password: str,
        ttl: timedelta,
    ) -> None:
        ...

    @abstractmethod
    async def get_password_by_email(
        self,
        email: EmailValue,
    ) -> str | None:
        ...