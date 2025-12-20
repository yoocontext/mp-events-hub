from dataclasses import dataclass
from typing import Any
from uuid import UUID
from dateutil.parser import isoparse # type: ignore

from elasticsearch import AsyncElasticsearch, ApiError

from modules.event.application.interfaces.projection_services import (
    IEventProjectionService,
)
from modules.event.application.projections.event import (
    EventProjection,
    AddressProjection,
    UpdateEventProjection,
)
from seedwork.domain.marker import EMPTY
from seedwork.domain.value_objects.paginator import (
    LimitPaginatorValue,
    OffsetPaginatorValue,
)
from seedwork.infra.elastic.exceptions import ElasticException


@dataclass
class EventProjectionElcService(IEventProjectionService):
    _elc: AsyncElasticsearch
    _index_name: str = "events.events"

    async def search(
        self,
        query: str | None = None,
        event_id: UUID | None = None,
        created_by_user_id: UUID | None = None,
        limit: LimitPaginatorValue = LimitPaginatorValue(25),
        offset: OffsetPaginatorValue = OffsetPaginatorValue(0),
    ) -> list[EventProjection]:
        es_query: dict[str, Any] = {"bool": {"must": [], "filter": []}}

        if query:
            es_query["bool"]["must"].append(
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title^3",
                            "title.translit^3",
                            "title.stem^3",
                            "description",
                            "description.translit",
                            "description.stem",
                            "created_by_fullname",
                            "created_by_fullname.translit",
                            "created_by_fullname.stem",
                            "full_address",
                        ],
                        "fuzziness": "AUTO",
                    }
                }
            )

        if event_id:
            es_query["bool"]["filter"].append(
                {
                    "term": {"id": str(event_id)}
                }
            )

        if created_by_user_id:
            es_query["bool"]["filter"].append(
                {
                    "term": {"created_by_id": str(created_by_user_id)}
                }
            )

        if not es_query["bool"]["must"] and not es_query["bool"]["filter"]:
            es_query = {"match_all": {}}

        resp = await self._elc.search(
            index=self._index_name,
            query=es_query,
            size=limit.value,
            from_=offset.value,
        )

        results: list[EventProjection] = []

        for hit in resp["hits"]["hits"]:
            source = hit["_source"]

            addr = source.get("address")
            address = AddressProjection(**addr) if addr else None

            scheduled_at_raw = source["scheduled_at"]
            scheduled_at = (
                isoparse(scheduled_at_raw)
                if isinstance(scheduled_at_raw, str)
                else scheduled_at_raw
            )

            image_id_raw = source.get("image_id")
            image_id = UUID(image_id_raw) if image_id_raw else None

            event_projection = EventProjection(
                id=UUID(source["id"]),
                title=source["title"],
                description=source["description"],
                created_by_fullname=source["created_by_fullname"],
                created_by_id=UUID(source["created_by_id"]),
                scheduled_at=scheduled_at,
                address=address,
                image_id=image_id,
            )

            results.append(event_projection)

        return results


    async def create(self, event: EventProjection) -> None:
        doc = {
            "id": str(event.id),
            "title": event.title,
            "description": event.description,
            "created_by_fullname": event.created_by_fullname,
            "created_by_id": str(event.created_by_id),
            "scheduled_at": event.scheduled_at.isoformat(),
            "image_id": str(event.image_id) if event.image_id else None,
            "address": {
                "city": event.address.city if event.address else None,
                "street": event.address.street if event.address else None,
                "building_number": event.address.building_number if event.address else None,
                "block": event.address.block if event.address else None,
                "auditorium": event.address.auditorium if event.address else None,
            } if event.address else None,
        }

        try:
            await self._elc.index(
                index=self._index_name,
                id=str(event.id),
                document=doc,
            )
        except ApiError:
            # todo add logging
            raise ElasticException()

    async def update(self, update: UpdateEventProjection) -> None:
        resp = await self._elc.get(index=self._index_name, id=str(update.id))
        source = resp["_source"]

        doc = {}

        if update.title is not EMPTY:
            doc["title"] = update.title if update.title is not None else None

        if update.description is not EMPTY:
            doc["description"] = update.description if update.description is not None else None

        if update.created_by_fullname is not EMPTY:
            doc["created_by_fullname"] = update.created_by_fullname if update.created_by_fullname is not None else None

        if update.created_by_id is not EMPTY:
            doc["created_by_id"] = str(update.created_by_id) if update.created_by_id is not None else None

        if update.scheduled_at is not EMPTY:
            doc["scheduled_at"] = update.scheduled_at.isoformat() if update.scheduled_at is not None else None

        if update.image_id is not EMPTY:
            doc["image_id"] = str(update.image_id) if update.image_id is not None else None

        if update.address is not EMPTY:
            addr_doc = {}
            addr = source.get("address") or {}
            upd_addr = update.address
            if upd_addr.city is not EMPTY:
                addr_doc["city"] = upd_addr.city
            if upd_addr.street is not EMPTY:
                addr_doc["street"] = upd_addr.street
            if upd_addr.building_number is not EMPTY:
                addr_doc["building_number"] = upd_addr.building_number
            if upd_addr.block is not EMPTY:
                addr_doc["block"] = upd_addr.block
            if upd_addr.auditorium is not EMPTY:
                addr_doc["auditorium"] = upd_addr.auditorium

            if addr_doc:
                doc["address"] = {**addr, **addr_doc}

        if doc:
            try:
                await self._elc.update(
                    index=self._index_name,
                    id=str(update.id),
                    doc=doc,
                )
            except ApiError:
                # todo add logging
                raise ElasticException()