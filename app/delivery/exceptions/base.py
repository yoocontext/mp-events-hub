from abc import (
    ABC,
    abstractmethod,
)

from seedwork.exceptions import AppException


DEFAULT_ERROR_CONTENT = {
    "application/json": {
        "example": {
            "detail": "string"
        }
    }
}


class DeliveryException(
    AppException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Presentation exception"