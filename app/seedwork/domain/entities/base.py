from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)

from seedwork.domain.uuid7 import uuid7_native
from seedwork.domain.value_objects.common.aggregate import EntityIdValue


@dataclass(
    kw_only=True,
    slots=True,
    init=False,
)
class Entity(ABC):
    id: EntityIdValue = field(
        default_factory=lambda: EntityIdValue(_value=uuid7_native()),
        repr=False,
    )

    @property
    def get_id(self) -> EntityIdValue:
        return self.id

    def __hash__(self) -> int:
        return hash(self.id.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            raise NotImplementedError

        return self.id == other.id


@dataclass(
    kw_only=True,
    slots=True,
    init=False,
)
class TimestampEntity(
    Entity,
    ABC,
):
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = field(default=None)

    @property
    def get_created_time(self) -> datetime:
        return self.created_at

    @property
    def get_updated_time(self) -> datetime | None:
        return self.updated_at

    def _touch(self) -> None:
        self.updated_at = datetime.now(tz=timezone.utc)