from dishka import Provider, Scope, provide

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.application.services.jwt import JwtService
from modules.auth.application.use_cases.confirm import ConfirmRegisterUseCase
from modules.auth.application.use_cases.confirm_reset import ConfirmResetPasswordUseCase
from modules.auth.application.use_cases.login import LoginUseCase
from modules.auth.application.use_cases.register import RegisterUseCase
from modules.auth.application.use_cases.reset_password import ResetPasswordUseCase
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.user import UniqueEmailRule, UniqueUserRule
from seedwork.application.interface.event_bus import IEventBus
from seedwork.infra.transaction_manager.base import ITransactionManager


class UseCaseAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def register(
        self,
        transaction_manager: ITransactionManager,
        user_repository: IUserRepository,
        user_kv_dm: IUserKvDm,
        unique_email_rule: UniqueEmailRule,
        unique_user_rule: UniqueUserRule,
        event_bus: IEventBus,
        ) -> RegisterUseCase:
        return RegisterUseCase(
            _transaction_manager=transaction_manager,
            _user_repository=user_repository,
            _user_kv_dm=user_kv_dm,
            _unique_email_rule=unique_email_rule,
            _unique_user_rule=unique_user_rule,
            _event_bus=event_bus,
        )

    @provide
    def confirm(
        self,
        jwt_service: JwtService,
        user_repo: IUserRepository,
        user_kv_dm: IUserKvDm,
        event_bus: IEventBus,
        transactional_manager: ITransactionManager,
    ) -> ConfirmRegisterUseCase:
        return ConfirmRegisterUseCase(
            _jwt_service=jwt_service,
            _user_repo=user_repo,
            _user_kv_dm=user_kv_dm,
            _event_bus=event_bus,
            _transactional_manager=transactional_manager,
        )

    @provide
    def login(
        self,
        user_repo: IUserRepository,
        jwt_service: JwtService,
    ) -> LoginUseCase:
        return LoginUseCase(
            _user_repo=user_repo,
            _jwt_service=jwt_service,
        )

    @provide
    def reset_password(
        self,
        user_repo: IUserRepository,
        user_dm: IUserKvDm,
        event_bus: IEventBus,
    ) -> ResetPasswordUseCase:
        return ResetPasswordUseCase(
            _user_repo=user_repo,
            _user_dm=user_dm,
            _event_bus=event_bus,
        )

    @provide
    def confirm_reset(
        self,
        jwt_service: JwtService,
        user_repo: IUserRepository,
        user_dm: IUserKvDm,
        transactional_manager: ITransactionManager,
    ) -> ConfirmResetPasswordUseCase:
        return ConfirmResetPasswordUseCase(
            _jwt_service=jwt_service,
            _user_repo=user_repo,
            _user_dm=user_dm,
            _transactional_manager=transactional_manager,
        )