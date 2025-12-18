from dataclasses import dataclass
from uuid import UUID

from modules.auth.domain.aggregate.user import User
from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.event_registration import EventRegistration
from modules.event.domain.repository.event import EventRepository
from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.domain.repository.user import IUserRepository
from modules.event.domain.services.event_registration import EventRegistrationService
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class RegisterForEventCommand:
    user_id: UUID
    event_id: UUID


@dataclass
class RegisterForEventUseCase(
    BaseUseCase[RegisterForEventCommand, EventRegistration],
):
    _event_registration_service: EventRegistrationService
    _event_repo: EventRepository
    _user_repo: IUserRepository
    _event_registration_repo: IEventRegistrationRepository
    _transactional_manager: ITransactionManager

    async def act(self, command: RegisterForEventCommand) -> EventRegistration:
        event: Event = await self._event_repo.get_by_id(
            _id=EntityIdValue(command.event_id),
        )
        user: User = await self._user_repo.get_by_id(
            required_id=EntityIdValue(command.user_id),
        )

        event_registration: EventRegistration = await (
            self._event_registration_service.register_user_for_event(
                user=user,
                event=event,
            )
        )

        await self._event_registration_repo.create(
            event_registration=event_registration,
        )

        await self._transactional_manager.commit()

        return event_registration