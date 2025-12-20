from abc import ABC, abstractmethod
from dataclasses import dataclass

from seedwork.infra.exception import InfraException


@dataclass
class ElasticException(
    InfraException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "ElasticSearch Exception"