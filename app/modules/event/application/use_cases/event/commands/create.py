from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.application.validators.event import EventImageValidator
from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.event import IEventRepository
from modules.event.domain.repository.user import IUserRepository
from seedwork.application.interface.s3.client import IS3Client
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.services.authorization import AuthorizationService
from seedwork.domain.uuid7 import uuid7_native
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.domain.value_objects.content_types import ContentType
from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.value_objects.s3 import Bucket
from seedwork.infra.s3.services.image_metadata import (
    ImageMetadataService,
    ImageMetadataSchema,
)
from seedwork.infra.s3.support_obj import AsyncFileStreamer, AsyncReadable
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class CreateEventCommand:
    user_id: UUID
    title: str
    scheduled_at: datetime
    description: str
    city: str
    street: str
    building_number: int
    block: str | None
    auditorium: str | None
    image_fileobject: AsyncReadable
    image_content_type: str


@dataclass
class CreateEventUseCase(
    BaseUseCase[CreateEventCommand, Event],
):
    _authorization_service: AuthorizationService
    _image_meta_service: ImageMetadataService
    _user_repo: IUserRepository
    _event_repo: IEventRepository
    _s3_client: IS3Client
    _event_image_validator: EventImageValidator
    _transactional_manager: ITransactionManager

    async def act(self, command: CreateEventCommand) -> Event:
        user: User = await self._user_repo.get_by_id(
            required_id=EntityIdValue(_value=command.user_id),
        )

        self._authorization_service.check_min_role(
            user_role=user.role,
            minimum_role=RoleValue.ORGANIZER,
        )

        image_metadata: ImageMetadataSchema = await self._image_meta_service.get(
            file=command.image_fileobject,
        )
        await self._event_image_validator.validate(
            content_type=command.image_content_type,
            height=image_metadata.height,
            wight=image_metadata.width,
        )

        image_uid: UUID = uuid7_native()
        file = AsyncFileStreamer(command.image_fileobject).to_generator()
        await self._s3_client.upload_stream(
            file=file,
            key=image_uid,
            bucket=Bucket.IMAGE,
            content_type=ContentType(command.image_content_type),
        )

        event: Event = user.create_event(
            title=command.title,
            scheduled_at=command.scheduled_at,
            description=command.description,
            image_id=image_uid,
            city=command.city,
            street=command.street,
            building_number=command.building_number,
            block=command.block,
            auditorium=command.auditorium,
        )

        await self._event_repo.create(event=event)

        await self._transactional_manager.commit()

        return event