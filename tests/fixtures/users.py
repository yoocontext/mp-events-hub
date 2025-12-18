from typing import Annotated

import pytest
from dishka import AsyncContainer

from modules.auth.application.services.jwt import JwtService
from modules.auth.domain.aggregate.user import User as UserAuth
from modules.auth.domain.repository.user import IUserRepository as IUserAuthRepository
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from modules.event.domain.repository.user import IUserRepository as IUserEventRepository
from modules.event.domain.aggregate.user import User as UserEvent
from seedwork.domain.events.base import DomainEvent
from seedwork.domain.value_objects.jwt import JwtTokenValue
from seedwork.domain.value_objects.role import RoleValue
from seedwork.application.interface.event_bus import IEventBus
from seedwork.infra.transaction_manager.base import ITransactionManager


@pytest.fixture(scope="session")
async def user_access_token(
    test_container: AsyncContainer,
) -> str:
    user = UserAuth.create(
        name="Sonya",
        second_name="Sqwirtick",
        group_number="241-251",
        email="sleeppy@gmail.com",
        password="qwerty123",
        role=RoleValue.USER,
        email_confirm=True,
    )

    token: str = await create_user(
        user_auth=user,
        test_container=test_container,
    )

    return token


@pytest.fixture(scope="session")
async def organizer_access_token(
    ioc_container: AsyncContainer,
) -> str:
    user = UserAuth.create(
        name="Dmitriy",
        second_name="Holod",
        group_number="231-251",
        email="vodka@gmail.com",
        password="123456",
        role=RoleValue.ORGANIZER,
        email_confirm=True,
    )

    token: str = await create_user(
        user_auth=user,
        test_container=ioc_container,
    )

    return token


@pytest.fixture(scope="session")
async def admin_access_token(
    test_container: AsyncContainer,
) -> str:
    user = UserAuth.create(
        name="Malenkiy",
        second_name="Yarche",
        group_number="231-361",
        email="bro@gmail.com",
        password="qwerty123",
        role=RoleValue.ADMIN,
        email_confirm=True,
    )

    token: str = await create_user(
        user_auth=user,
        test_container=test_container,
    )

    return token


async def create_user(
    user_auth: UserAuth,
    test_container: AsyncContainer,
) -> Annotated[str, "access_token"]:
    async with test_container() as cont:
        jwt_service: JwtService = await cont.get(JwtService)
        user_auth_repo: IUserAuthRepository = await cont.get(IUserAuthRepository)
        user_event_repo: IUserEventRepository = await cont.get(IUserEventRepository)
        transactional_manager: ITransactionManager = await (
            cont.get(ITransactionManager)
        )
        event_bus: IEventBus = await cont.get(IEventBus)

        user_auth.confirm_register(
            input_code=ConfirmCodeValue("test"),
            stored_code=ConfirmCodeValue("test"),
        )
        await user_auth_repo.create(user_auth)

        user_event = UserEvent(
            id=user_auth.id,
            created_at=user_auth.created_at,
            updated_at=user_auth.updated_at,
            role=user_auth.role,
        )
        await user_event_repo.create(user_event)

        events: list[DomainEvent] = user_auth.pull_events()

        await event_bus.publish(events)
        await transactional_manager.commit()

        token: JwtTokenValue = jwt_service.issue_token(
            payload={"user_id": str(user_auth.id.value)},
        )

        return token.value