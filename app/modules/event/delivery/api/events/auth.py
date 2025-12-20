from faststream.rabbit import RabbitRouter

from bootstrap.ioc import get_container
from modules.event.application.use_cases.auth.confirm import (
    ConfirmRegisterUseCase,
    ConfirmRegisterCommand,
)
from modules.event.application.use_cases.event.reactors.create_event import (
    CreateEventElasticUseCase,
    CreateEventElasticCommand,
)
from seedwork.domain.events.auth import ConfirmRegistrationUserEvent
from seedwork.domain.events.events import CreateEventEvent
from seedwork.infra.rmq.queues import CONFIRM_REGISTRATION_USER_EVENT_QUEUE, EVENT_EVENT_CREATE_QUEUE

router = RabbitRouter()


@router.subscriber(
    queue=CONFIRM_REGISTRATION_USER_EVENT_QUEUE,
)
async def confirm_registration_user(
    event: ConfirmRegistrationUserEvent,
) -> None:
    """Event driven replication of the user’s role"""

    container = get_container()

    async with container() as cont:
        use_case: ConfirmRegisterUseCase = await cont.get(ConfirmRegisterUseCase)
        command = ConfirmRegisterCommand(
            user_id=event.user_id,
            role=event.role,
        )

        await use_case.act(command)


@router.subscriber(
    queue=EVENT_EVENT_CREATE_QUEUE,
)
async def create_event_elastic(
    event: CreateEventEvent,
) -> None:
    """Event-driven replication of the domain event to the read model in Elasticsearch"""

    container = get_container()

    async with container() as cont:
        use_case: CreateEventElasticUseCase = await cont.get(CreateEventElasticUseCase)
        command = CreateEventElasticCommand(
            id=event.id,
            created_at=event.created_at,
            created_by_user_id=event.created_by_user_id,
            title=event.title,
            scheduled_at=event.scheduled_at,
            description=event.description,
            image_id=event.image_id,
            city=event.city,
            street=event.street,
            building_number=event.building_number,
            block=event.block,
            auditorium=event.auditorium,
        )

        await use_case.act(command=command)