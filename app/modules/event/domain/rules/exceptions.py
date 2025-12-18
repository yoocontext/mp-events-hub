from dataclasses import dataclass

from seedwork.domain.rules import BusinessRuleException
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


@dataclass
class UserAlreadyRegisteredException(BusinessRuleException):
    user_id: EntityIdValue
    event_id: EntityIdValue

    @property
    def message(self) -> str:
        return (
            f"Пользователь '{self.user_id}' уже зарегистрирован на событие '{self.event_id}'."
        )
