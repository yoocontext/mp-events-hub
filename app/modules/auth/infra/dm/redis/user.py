from asyncpg.pgproto.pgproto import timedelta

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.user import EmailValue
from seedwork.infra.dm.base import BaseRedisDataMapper


class UserRedisDm(
    IUserKvDm,
    BaseRedisDataMapper,
):
    async def save_confirm_code_by_id(
        self,
        user_id: EntityIdValue,
        confirm_code: ConfirmCodeValue,
        ttl: timedelta,
    ) -> None:
        await self._redis.set(
            name=f"user:confirm:{user_id.value}",
            value=confirm_code.value,
            ex=ttl,
        )

    async def get_confirm_code_by_id(
        self,
        user_id: EntityIdValue,
    ) -> str | None:
        code = await self._redis.get(f"user:confirm:{user_id.value}")

        if code is None:
            return None

        return code.decode()

    async def save_confirm_code_by_email(
        self,
        email: EmailValue,
        confirm_code: ConfirmCodeValue,
        ttl: timedelta,
    ) -> None:
        await self._redis.set(
            name=f"user:confirm:{email.value}",
            value=confirm_code.value,
            ex=ttl,
        )

    async def get_confirm_code_by_email(
        self,
        email: EmailValue,
    ) -> str | None:
        code = await self._redis.get(f"user:confirm:{email.value}")

        if code is None:
            return None

        return code.decode()

    async def save_password_by_email(
        self,
        email: EmailValue,
        password: str,
        ttl: timedelta,
    ) -> None:
        await self._redis.set(
            name=f"user:password:{email.value}",
            value=password,
            ex=ttl,
        )
    async def get_password_by_email(
        self,
        email: EmailValue,
    ) -> str | None:
        password = await self._redis.get(f"user:password:{email.value}")

        if password is None:
            return None

        return password.decode()