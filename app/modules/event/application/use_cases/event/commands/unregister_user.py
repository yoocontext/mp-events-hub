from dataclasses import dataclass
from uuid import UUID

from modules.event.domain.aggregate.event_registration import EventRegistration
from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.domain.services.event_registration import (
    EventRegistrationService,
)
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class UnregisterForEventCommand:
    event_id: UUID
    user_id: UUID


@dataclass
class UnregisterForEventUseCase(
    BaseUseCase[UnregisterForEventCommand, None],
):
    _event_registration_service: EventRegistrationService
    _event_registration_repo: IEventRegistrationRepository
    _transactional_manager: ITransactionManager

    async def act(self, command: UnregisterForEventCommand) -> None:
        registration: EventRegistration = await (
            self._event_registration_service.unregister_user_for_event(
                user_id=EntityIdValue(command.user_id),
                event_id=EntityIdValue(command.event_id),
            )
        )

        await self._event_registration_repo.delete(
            event_registration=registration,
        )

        await self._transactional_manager.commit()
