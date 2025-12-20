from modules.event.application.projections.event import (
    EventProjection,
)
from modules.event.delivery.api.http.v1.events.schemas import (
    GetEventOutSchema,
    EventSchema,
    AddressSchema,
)


def event_projections_to_out_schema(
    projections: list[EventProjection],
) -> GetEventOutSchema:
    event_schemas: list[EventSchema] = []

    for prj in projections:

        address: AddressSchema | None = None
        if prj.address:
            address = AddressSchema(
                city=prj.address.city,
                street=prj.address.street,
                building_number=prj.address.building_number,
                block=prj.address.block,
                auditorium=prj.address.auditorium,
            )

        event = EventSchema(
            id=prj.id,
            title=prj.title,
            description=prj.description,
            created_by_id=prj.created_by_id,
            created_by_fullname=prj.created_by_fullname,
            scheduled_at=prj.scheduled_at,
            image_id=prj.image_id,
            address=address,
        )

        event_schemas.append(event)

    return GetEventOutSchema(events=event_schemas)