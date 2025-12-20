from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from modules.event.domain.aggregate.exceptions import (
    AddressFormatException,
    DeleteNotAllowed,
    OrganizerCannotDeleteForeignEvent,
)
from modules.event.domain.value_objects.address import (
    AddressValue,
    CityValue,
    StreetValue,
    BuildingValue,
    BuildingNumberValue,
    BuildingBlockValue,
    AuditoriumValue,
)
from modules.event.domain.value_objects.event import (
    TitleValue,
    ScheduledAtValue,
    DescriptionValue,
)
from modules.event.domain.value_objects.exceptions import EventInPastException
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.events.events import DeleteEventEvent, CreateEventEvent
from seedwork.domain.marker import EMPTY
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.value_objects.s3 import S3IdValue


@dataclass
class Event(BaseAggregate):
    created_by_user_id: EntityIdValue
    title: TitleValue
    scheduled_at: ScheduledAtValue
    address: AddressValue | None
    description: DescriptionValue
    image_id: S3IdValue

    @classmethod
    def create(
        cls,
        created_by_user_id: UUID,
        title: str,
        scheduled_at: datetime,
        description: str,
        image_id: UUID,
        city: str | None,
        street: str | None,
        building_number: int | None,
        block: str | None,
        auditorium: str | None,
    ) -> "Event":
        dt_now: datetime = datetime.now(tz=timezone.utc)

        if scheduled_at < dt_now:
            raise EventInPastException(value=scheduled_at)

        if 3 > sum(v is not None for v in [city, street, building_number]) > 0:
            raise AddressFormatException(
                city=city,
                street=street,
                building_number=building_number,
            )

        address_vo: AddressValue | None = None

        if city and street and building_number is not None:
            block_vo: BuildingBlockValue | None = (
                BuildingBlockValue(block)) if block else None

            auditorium_vo: AuditoriumValue | None = (
                AuditoriumValue(auditorium)) if auditorium else None

            building_vo = BuildingValue(
                number=BuildingNumberValue(_value=building_number),
                block=block_vo,
                auditorium=auditorium_vo,
            )

            address_vo = AddressValue(
                city=CityValue(_value=city),
                street=StreetValue(_value=street),
                building=building_vo,
            )

        event = Event(
            created_by_user_id=EntityIdValue(created_by_user_id),
            title=TitleValue(title),
            scheduled_at=ScheduledAtValue(scheduled_at),
            address=address_vo,
            description=DescriptionValue(description),
            image_id=S3IdValue(image_id),
        )

        create_event = CreateEventEvent(
            id=event.id.value,
            created_at=event.created_at,
            created_by_user_id=event.created_by_user_id.value,
            title=event.title.value,
            scheduled_at=event.scheduled_at.value,
            description=event.description.value,
            image_id=event.image_id.value,
            city=city,
            street=street,
            building_number=building_number,
            block=block,
            auditorium=auditorium,
        )

        event.register_event(event=create_event)

        return event

    def delete(
        self,
        requester_user_id: EntityIdValue,
        requester_role: RoleValue,
    ) -> None:
        if requester_role == RoleValue.USER:
            raise DeleteNotAllowed(
                role=requester_role.value,
            )

        is_organizer = requester_role != RoleValue.ORGANIZER
        user_not_equal = self.created_by_user_id != requester_user_id

        if is_organizer and user_not_equal:
            raise OrganizerCannotDeleteForeignEvent()

        event = DeleteEventEvent(d_event_id=self.id.value)
        self.register_event(event)

    def update(
        self,
        requester_user_id: UUID,
        requester_role: RoleValue,
        title: str | None,
        scheduled_at: datetime | None,
        description: str | None,
        image_id: str | None,
        city: str | None,
        street: str | None,
        building_number: int | None,
        block: str | None,
        auditorium: str | None,
    ) -> None:
        # check role
        if requester_role == RoleValue.USER:
            raise DeleteNotAllowed(
                role=requester_role.value,
            )

        is_organizer = requester_role != RoleValue.ORGANIZER
        user_not_equal = self.created_by_user_id != requester_user_id

        if is_organizer and user_not_equal:
            raise OrganizerCannotDeleteForeignEvent()

        # check other rules
        dt_now: datetime = datetime.now(tz=timezone.utc)

        if title is not EMPTY:
            self.title = TitleValue(title)

        if scheduled_at is not EMPTY:
            if scheduled_at is not None and scheduled_at < dt_now:
                raise EventInPastException(value=scheduled_at)

            self.scheduled_at = ScheduledAtValue(scheduled_at)

        if description is not EMPTY:
            self.description = DescriptionValue(description)

        if image_id is not EMPTY:
            self.image_id = S3IdValue(image_id)

        if any(arg is not EMPTY for arg in [city, street, building_number, block, auditorium]):

            new_city = city if city is not EMPTY else self.address.city._value if self.address else None
            new_street = street if street is not EMPTY else self.address.street._value if self.address else None
            new_building_number = building_number if building_number is not EMPTY else (
                self.address.building.number._value if self.address and self.address.building.number else None
            )
            new_block = block if block is not EMPTY else (
                self.address.building.block._value if self.address and self.address.building.block else None
            )
            new_auditorium = auditorium if auditorium is not EMPTY else (
                self.address.building.auditorium._value if self.address and self.address.building.auditorium else None
            )

            if 3 > sum(v is not None for v in [new_city, new_street, new_building_number]) > 0:
                raise AddressFormatException(
                    city=new_city,
                    street=new_street,
                    building_number=new_building_number,
                )

            address_vo: AddressValue | None = None
            if new_city and new_street and new_building_number is not None:
                building_vo = BuildingValue(
                    number=BuildingNumberValue(new_building_number),
                    block=BuildingBlockValue(new_block) if new_block else None,
                    auditorium=AuditoriumValue(new_auditorium) if new_auditorium else None,
                )
                address_vo = AddressValue(
                    city=CityValue(new_city),
                    street=StreetValue(new_street),
                    building=building_vo,
                )

            self.address = address_vo