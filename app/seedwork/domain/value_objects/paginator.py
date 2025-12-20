from seedwork.domain.value_objects.common.base import BaseSimpleValueObject
from seedwork.domain.value_objects.validators.numbers import (
    is_positive,
    is_non_negative,
)


class LimitPaginatorValue(BaseSimpleValueObject[int, int]):
    def validate(self) -> None:
        is_positive(self._value)


class OffsetPaginatorValue(BaseSimpleValueObject[int, int]):
    def validate(self) -> None:
        is_non_negative(self._value)