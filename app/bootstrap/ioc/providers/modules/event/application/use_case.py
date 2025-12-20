from dishka import Provider, Scope, provide

from modules.event.application.interfaces.projection_services import IEventProjectionService
from modules.event.application.use_cases.event.commands.create import (
    CreateEventUseCase,
)
from modules.event.application.use_cases.auth.confirm import (
    ConfirmRegisterUseCase,
)
from modules.event.application.use_cases.event.commands.delete import (
    DeleteEventUseCase,
)
from modules.event.application.use_cases.event.commands.register_user import (
    RegisterForEventUseCase,
)
from modules.event.application.use_cases.event.commands.unregister_user import (
    UnregisterForEventUseCase,
)
from modules.event.application.use_cases.event.commands.update import (
    UpdateEventUseCase,
)
from modules.event.application.use_cases.event.queries.events import (
    GetEventProjectionUseCase,
)
from modules.event.application.use_cases.event.reactors.create_event import CreateEventElasticUseCase
from modules.event.application.validators.event import EventImageValidator
from modules.event.domain.repository.event import IEventRepository
from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.domain.repository.user import IUserRepository
from modules.event.domain.services.event_registration import EventRegistrationService
from seedwork.application.interface.s3.client import IS3Client
from seedwork.domain.services.authorization import AuthorizationService
from seedwork.infra.event_bus.base import IEventBus
from seedwork.infra.s3.services.image_metadata import ImageMetadataService
from seedwork.infra.transaction_manager.base import ITransactionManager


class UseCaseEventProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def create_event(
        self,
        authorization_service: AuthorizationService,
        image_meta_service: ImageMetadataService,
        user_repo: IUserRepository,
        event_repo: IEventRepository,
        s3_client: IS3Client,
        event_image_validator: EventImageValidator,
        transactional_manager: ITransactionManager,
        event_bus: IEventBus,
    ) -> CreateEventUseCase:
        return CreateEventUseCase(
            _authorization_service=authorization_service,
            _image_meta_service=image_meta_service,
            _user_repo=user_repo,
            _event_repo=event_repo,
            _s3_client=s3_client,
            _event_image_validator=event_image_validator,
            _transactional_manager=transactional_manager,
            _event_bus=event_bus,
        )

    @provide
    def delete_event(
        self,
        s3_client: IS3Client,
        event_repo: IEventRepository,
        user_repo: IUserRepository,
        transactional_manager: ITransactionManager,
    ) -> DeleteEventUseCase:
        return DeleteEventUseCase(
            _s3_client=s3_client,
            _event_repo=event_repo,
            _user_repo=user_repo,
            _transactional_manager=transactional_manager,
        )

    @provide
    def update_event(
        self,
        s3_client: IS3Client,
        image_metadata_service: ImageMetadataService,
        event_image_validator: EventImageValidator,
        event_repo: IEventRepository,
        user_repo: IUserRepository,
        transactional_manager: ITransactionManager,
    ) -> UpdateEventUseCase:
        return UpdateEventUseCase(
            _s3_client=s3_client,
            _image_metadata_service=image_metadata_service,
            _event_image_validator=event_image_validator,
            _event_repo=event_repo,
            _user_repo=user_repo,
            _transactional_manager=transactional_manager,
        )

    @provide
    def confirm_register(
        self,
        user_repo: IUserRepository,
        transaction_manager: ITransactionManager,
    ) -> ConfirmRegisterUseCase:
        return ConfirmRegisterUseCase(
            _user_repo=user_repo,
            _transaction_manager=transaction_manager,
        )

    @provide
    def register_for_event(
        self,
        event_registration_service: EventRegistrationService,
        event_repo: IEventRepository,
        user_repo: IUserRepository,
        event_registration_repo: IEventRegistrationRepository,
        transactional_manager: ITransactionManager,
    ) -> RegisterForEventUseCase:
        return RegisterForEventUseCase(
            _event_registration_service=event_registration_service,
            _event_repo=event_repo,
            _user_repo=user_repo,
            _event_registration_repo=event_registration_repo,
            _transactional_manager=transactional_manager,
        )

    @provide
    def unregister_for_event(
        self,
        event_registration_service: EventRegistrationService,
        event_registration_repo: IEventRegistrationRepository,
        transactional_manager: ITransactionManager,
    ) -> UnregisterForEventUseCase:
        return UnregisterForEventUseCase(
            _event_registration_service=event_registration_service,
            _event_registration_repo=event_registration_repo,
            _transactional_manager=transactional_manager,
        )

    @provide
    def get_events(
        self,
        projection_service: IEventProjectionService,
    ) -> GetEventProjectionUseCase:
        return GetEventProjectionUseCase(
            _event_query_service=projection_service,
        )

    @provide
    def create_event_elastic(
        self,
        event_projection_service: IEventProjectionService,
    ) -> CreateEventElasticUseCase:
        return CreateEventElasticUseCase(
            _event_projection_service=event_projection_service,
        )