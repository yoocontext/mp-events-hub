from seedwork.domain.events.base import DomainEvent
from seedwork.infra.event_bus.base import QueueRmq

from seedwork.domain.events.auth import (
    RequestedRegistrationUserEvent,
    ConfirmRegistrationUserEvent,
    RequestResetPasswordEvent,
)
from seedwork.domain.events.events import (
    CreateEventEvent,
)
from seedwork.infra.rmq.queues import (
    REQUESTED_REGISTRATION_USER_EVENT_QUEUE,
    CONFIRM_REGISTRATION_USER_EVENT_QUEUE,
    REQUESTED_RESET_PASSWORD_USER_EVENT_QUEUE,
    EVENT_EVENT_CREATE_QUEUE,
)

event_queue_map: dict[type[DomainEvent], QueueRmq] = {
    RequestedRegistrationUserEvent: REQUESTED_REGISTRATION_USER_EVENT_QUEUE,
    ConfirmRegistrationUserEvent: CONFIRM_REGISTRATION_USER_EVENT_QUEUE,
    RequestResetPasswordEvent: REQUESTED_RESET_PASSWORD_USER_EVENT_QUEUE,
    CreateEventEvent: EVENT_EVENT_CREATE_QUEUE,
}