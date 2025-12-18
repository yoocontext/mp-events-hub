from dataclasses import asdict, fields, is_dataclass
from typing import TypeVar, cast

from seedwork.domain.events.base import DomainEvent
from seedwork.domain.event_store import EventTypeMap
from seedwork.infra.pg.models.event_store import StoredEventOrm


TEvent = TypeVar("TEvent", bound=DomainEvent)


class EventAlchemyMapper:
    @staticmethod
    def to_orm(event: TEvent) -> StoredEventOrm:
        full_dict = asdict(event)
        payload = {
            k: v for k, v in full_dict.items() if
            k not in (
                "id", "type", "version", "aggregate_id", "aggregate_version", "created_at"
            )
        }
        return StoredEventOrm(
            event_id=event.id,
            event_type=event.type,
            event_version=event.version,
            aggregate_id=event.aggregate_id,
            aggregate_version=event.aggregate_version,
            created_at=event.created_at,
            payload=payload,
        )

    @staticmethod
    def from_orm(
        stored_orm: StoredEventOrm,
        event_map: EventTypeMap,
    ) -> TEvent:
        event_type: type[DomainEvent] = event_map.get(
            event_type=stored_orm.event_type,
            version=stored_orm.event_version,
        )

        if not is_dataclass(event_type):
            raise TypeError(f"{event_type} is not a dataclass")

        payload: dict = stored_orm.payload.copy()

        payload.update(
            {
                "id": stored_orm.event_id,
                "type": stored_orm.event_type,
                "version": stored_orm.event_version,
                "aggregate_id": stored_orm.aggregate_id,
                "aggregate_version": stored_orm.aggregate_version,
                "created_at": stored_orm.created_at,
            }
        )

        event_t = cast(type[TEvent], event_type)

        valid_fields = {f.name for f in fields(event_t)}
        payload = {k: v for k, v in payload.items() if k in valid_fields}

        return event_t(**payload)