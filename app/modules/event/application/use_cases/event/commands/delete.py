from dataclasses import dataclass
from uuid import UUID

from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.event import EventRepository
from modules.event.domain.repository.user import IUserRepository
from seedwork.application.interface.s3.client import IS3Client
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.common.aggregate import EntityIdValue
from seedwork.domain.value_objects.s3 import Bucket
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class DeleteEventCommand:
    event_id: UUID
    user_id: UUID


@dataclass
class DeleteEventUseCase(
    BaseUseCase[DeleteEventCommand, None],
):
    _s3_client: IS3Client
    _event_repo: EventRepository
    _user_repo: IUserRepository
    _transactional_manager: ITransactionManager

    async def act(self, command: DeleteEventCommand) -> None:
        event: Event = await self._event_repo.get_by_id(
            _id=EntityIdValue(command.event_id),
        )
        user: User = await self._user_repo.get_by_id(
            required_id=EntityIdValue(command.user_id),
        )

        event.delete(
            requester_user_id=user.id,
            requester_role=user.role,
        )

        await self._s3_client.delete(
            key=event.image_id.value,
            bucket=Bucket.IMAGE,
        )
        await self._event_repo.delete(_id=event.id)

        await self._transactional_manager.commit()