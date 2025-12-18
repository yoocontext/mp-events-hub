from dataclasses import dataclass, field

from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from seedwork.domain.rules import BusinessRule
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


@dataclass
class UserRegisteredEventRule(BusinessRule):
    _event_registration_repo: IEventRegistrationRepository

    __message: str = field(default="", init=False)

    async def is_broken(
        self,
        user_id: EntityIdValue,
        event_id: EntityIdValue,
    ) -> bool:
        is_exists: bool = await self._event_registration_repo.exists(
            user_id=user_id,
            event_id=event_id,
        )

        return is_exists
