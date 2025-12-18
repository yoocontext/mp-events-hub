from abc import ABC, abstractmethod

from seedwork.domain.exception import DomainException


class AggregateException(
    DomainException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Aggregate Exception"


class AggregateAlreadyCreatedException(AggregateException):
    @property
    def message(self) -> str:
        return "Агрегат уже создан, повторное создание запрещено"