from dataclasses import dataclass
from datetime import timedelta
from typing import cast

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.exceptions import UserNotFoundException
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.events.base import DomainEvent
from seedwork.domain.value_objects.user import EmailValue
from seedwork.application.interface.event_bus import IEventBus


@dataclass
class ResetPasswordCommand:
    email: str
    new_password: str
    confirm_code_ttl: timedelta


@dataclass
class ResetPasswordUseCase(
    BaseUseCase[ResetPasswordCommand, None],
):
    _user_repo: IUserRepository
    _user_dm: IUserKvDm
    _event_bus: IEventBus

    async def act(self, command: ResetPasswordCommand) -> None:
        email = EmailValue(command.email)
        user: User | None = await self._user_repo.find_by_email(
            email=email,
        )

        if not user:
            raise UserNotFoundException(email=command.email)

        user = cast(User, user)

        confirm_code: ConfirmCodeValue = user.reset_password_request(
            email=email,
        )

        await self._user_dm.save_confirm_code_by_email(
            email=email,
            confirm_code=confirm_code,
            ttl=command.confirm_code_ttl,
        )
        await self._user_dm.save_password_by_email(
            email=email,
            password=command.new_password,
            ttl=command.confirm_code_ttl,
        )

        events: list[DomainEvent] = user.pull_events()
        await self._event_bus.publish(events)