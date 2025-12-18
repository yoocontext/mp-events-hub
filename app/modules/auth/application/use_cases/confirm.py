from dataclasses import dataclass
from uuid import UUID

from modules.auth.application.exceptions import ConfirmCodeNotFoundException
from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.application.services.jwt import JwtService
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.events.base import DomainEvent
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.jwt import JwtTokenValue
from seedwork.application.interface.event_bus import IEventBus
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class ConfirmRegisterCommand:
    user_id: UUID
    confirm_code: str


@dataclass
class ConfirmRegisterUseCase(
    BaseUseCase[ConfirmRegisterCommand, JwtTokenValue],
):
    _jwt_service: JwtService
    _user_repo: IUserRepository
    _user_kv_dm: IUserKvDm
    _event_bus: IEventBus
    _transactional_manager: ITransactionManager

    async def act(self, command: ConfirmRegisterCommand) -> JwtTokenValue:
        user_id = EntityIdValue(_value=command.user_id)
        input_code = ConfirmCodeValue(_value=command.confirm_code)

        user: User = await self._user_repo.find_by_id(required_id=user_id)

        stored_code: str | None = await (
            self._user_kv_dm.get_confirm_code_by_id(user_id=user_id)
        )

        if not stored_code:
            raise ConfirmCodeNotFoundException()

        stored_code_value = ConfirmCodeValue(_value=stored_code)

        user.confirm_register(
            input_code=input_code,
            stored_code=stored_code_value,
        )

        token: JwtTokenValue = self._jwt_service.issue_token(
            payload={"user_id": str(user.id.value)},
        )

        await self._user_repo.update(user=user)
        await self._transactional_manager.commit()

        events: list[DomainEvent] = user.pull_events()
        await self._event_bus.publish(events)

        return token

