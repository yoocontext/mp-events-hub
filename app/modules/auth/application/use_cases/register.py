from dataclasses import dataclass
from datetime import timedelta

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.user import UniqueEmailRule, UniqueUserRule
from modules.auth.domain.rules.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.domain.value_objects.role import RoleValue
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.events.base import DomainEvent
from seedwork.application.interface.event_bus import IEventBus
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class RegisterCommand:
    name: str
    second_name: str
    group_number: str
    email: str
    password: str
    confirm_code_ttl: timedelta


@dataclass
class RegisterUseCase(
    BaseUseCase[RegisterCommand, User],
):
    _transaction_manager: ITransactionManager
    _user_repository: IUserRepository
    _user_kv_dm: IUserKvDm
    _unique_email_rule: UniqueEmailRule
    _unique_user_rule: UniqueUserRule
    _event_bus: IEventBus

    async def act(self, command: RegisterCommand) -> User:
        user: User = User.create(
            name=command.name,
            second_name=command.second_name,
            group_number=command.group_number,
            email=command.email,
            password=command.password,
            role=RoleValue.USER,
            email_confirm=False,
        )

        if await self._unique_email_rule.is_broken(email=user.email):
            raise EmailAlreadyExistsException(email=user.email)

        if await self._unique_user_rule.is_broken(
            name=user.name,
            second_name=user.second_name,
            group_number=user.group_number,
        ):
            raise UserAlreadyExistsException(
                name=user.name,
                second_name=user.second_name,
                group_number=user.group_number,
            )

        confirm_code: ConfirmCodeValue = user.unconfirmed_registration()

        await self._user_kv_dm.save_confirm_code_by_id(
            user_id=user.id,
            confirm_code=confirm_code,
            ttl=command.confirm_code_ttl,
        )

        await self._user_repository.create(user=user)

        await self._transaction_manager.commit()

        events: list[DomainEvent] = user.pull_events()
        await self._event_bus.publish(events=events)

        return user