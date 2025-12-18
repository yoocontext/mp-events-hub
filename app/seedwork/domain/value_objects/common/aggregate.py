from dataclasses import dataclass
from typing import Any

from seedwork.domain.value_objects.common.base import BaseSimpleValueObject
from seedwork.domain.value_objects.validators.numbers import is_positive


@dataclass(
    frozen=True,
    slots=True,
)
class EntityIdValue(BaseSimpleValueObject[Any, Any]):
    pass


@dataclass(
    frozen=True,
    slots=True,
)
class AggregateVersion(BaseSimpleValueObject[int, int]):
    def validate(self) -> None:
        is_positive(value=self.value)

    def next(self) -> "AggregateVersion":
        return AggregateVersion(self.value + 1)

    @classmethod
    def initial(cls) -> "AggregateVersion":
        return cls(0)