from dataclasses import dataclass

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.event_store import IEventStore, EventTypeMap
from seedwork.domain.events.base import DomainEvent
from seedwork.domain.value_objects.common.aggregate import (
    EntityIdValue,
    AggregateVersion,
)
from seedwork.infra.event_store.event_mapper import EventAlchemyMapper
from seedwork.infra.pg.models.event_store import StoredEventOrm


@dataclass
class EventStoreAlchemy(IEventStore):
    _event_mapper: EventAlchemyMapper
    _session: AsyncSession

    async def save(
        self,
        events: list[DomainEvent],
    ) -> None:
        events_orm: list[StoredEventOrm] = []
        events.sort(key=lambda x: x.aggregate_version)

        for event in events:
            event_orm: StoredEventOrm = self._event_mapper.to_orm(event=event)
            events_orm.append(event_orm)

        self._session.add_all(events_orm)

    async def load(
        self,
        aggregate_id: EntityIdValue,
        event_map: EventTypeMap,
    ) -> list[DomainEvent]:
        result = await self._session.execute(
            select(StoredEventOrm)
            .where(StoredEventOrm.aggregate_id == aggregate_id.value)
            .order_by(StoredEventOrm.aggregate_version)
        )

        events_orm: list[StoredEventOrm] = list(result.scalars().all())

        events: list[DomainEvent] = [
            self._event_mapper.from_orm(stored_orm=stored_orm, event_map=event_map)
            for stored_orm in events_orm
        ]

        return events

    async def get_current_agg_version(
        self,
        aggregate_id: EntityIdValue,
    ) -> AggregateVersion:
        result = await self._session.execute(
            select(StoredEventOrm.aggregate_version)
            .where(StoredEventOrm.aggregate_id == aggregate_id.value)
            .order_by(
                desc(StoredEventOrm.aggregate_version)
            )
            .limit(1)
        )

        current_agg_version: int = result.scalar_one()

        return AggregateVersion(current_agg_version)