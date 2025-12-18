from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.application.validators.event import EventImageValidator
from modules.event.domain.repository.user import IUserRepository
from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.event import EventRepository
from seedwork.application.interface.s3.client import IS3Client
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.content_types import ContentType
from seedwork.domain.value_objects.s3 import Bucket
from seedwork.infra.s3.services.image_metadata import (
    ImageMetadataService,
    ImageMetadataSchema,
)
from seedwork.infra.s3.support_obj import (
    AsyncReadable,
    AsyncFileStreamer,
)
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class UpdateEventCommand:
    event_id: UUID
    user_id: UUID
    title: str | None
    scheduled_at: datetime | None
    description: str | None
    city: str | None
    street: str | None
    building_number: int | None
    block: str | None
    auditorium: str | None
    image_fileobject: AsyncReadable | None
    image_content_type: str | None


@dataclass
class UpdateEventUseCase(
    BaseUseCase[UpdateEventCommand, Event],
):
    _s3_client: IS3Client
    _image_metadata_service: ImageMetadataService
    _event_repo: EventRepository
    _user_repo: IUserRepository
    _event_image_validator: EventImageValidator
    _transactional_manager: ITransactionManager

    async def act(
        self,
        command: UpdateEventCommand,
    ) -> Event:
        event: Event = await self._event_repo.get_by_id(
            _id=EntityIdValue(command.event_id),
        )
        user: User = await self._user_repo.get_by_id(
            required_id=EntityIdValue(command.user_id),
        )

        image_id: UUID | None = None
        content_type: ContentType | None = None
        stream: AsyncGenerator[bytes, None] | None = None

        if command.image_fileobject:
            image_metadata: ImageMetadataSchema = await self._image_metadata_service.get(
                file=command.image_fileobject,
            )
            await self._event_image_validator.validate(
                content_type=command.image_content_type,
                height=image_metadata.height,
                wight=image_metadata.width,
            )

            image_id = event.image_id.value
            content_type = ContentType(command.image_content_type)
            stream = AsyncFileStreamer(command.image_fileobject).to_generator()

        event.update(
            requester_user_id=user.id.value,
            requester_role=user.role,
            title=command.title,
            scheduled_at=command.scheduled_at,
            description=command.description,
            image_id=image_id,
            city=command.city,
            street=command.street,
            building_number=command.building_number,
            block=command.block,
            auditorium=command.auditorium,
        )

        event = await self._event_repo.update(event)

        if command.image_fileobject:
            await self._s3_client.upload_stream(
                file=stream,
                key=image_id,
                bucket=Bucket.IMAGE,
                content_type=content_type
            )

        await self._transactional_manager.commit()

        return event