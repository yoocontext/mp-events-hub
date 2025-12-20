from seedwork.domain.types import Number
from seedwork.domain.value_objects.common.base import ValueType
from seedwork.domain.value_objects.common.exceptions import NotPositiveNumberException, InvalidNumberTypeException


def is_positive(value: ValueType) -> None:
    if not isinstance(value, Number):
        raise InvalidNumberTypeException()

    if value <= 0:
        raise NotPositiveNumberException(value=value)


def is_non_negative(value: ValueType) -> None:
    if not isinstance(value, Number):
        raise InvalidNumberTypeException()

    if value < 0:
        raise NotPositiveNumberException(value=value)