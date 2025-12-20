"""
auth(bound-context).user(entity).requested-registration(act).event(type)
"""

REQUESTED_REGISTRATION_USER_EVENT_QUEUE: str = "auth.user.requested-registration.event"
CONFIRM_REGISTRATION_USER_EVENT_QUEUE: str = "auth.user.confirm-registration.event"
REQUESTED_RESET_PASSWORD_USER_EVENT_QUEUE: str = "auth.user.requested-reset.event"

EVENT_EVENT_CREATE_QUEUE: str = "event.event.create.event"
