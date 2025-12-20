from dishka import (
    AsyncContainer,
    Provider,
    make_async_container,
)
from dishka.integrations.fastapi import FastapiProvider

from bootstrap.ioc.providers.bootstrap import(
    SettingProvider,
)
from bootstrap.ioc.providers.infra import (
    ElasticSearchProvider,
    AlchemyProvider,
    EventBusProvider,
    FastStreamProvider,
    RedisProvider,
    S3ServicesProvider,
    S3Provider,
)
from bootstrap.ioc.providers.modules.auth import (
    RulesAuthProvider,
    RepositoryAuthProvider,
    MapperAuthProvider,
    ServiceAuthProvider,
    UseCaseAuthProvider,
    DmAlchemyAuthProvider,
    DmRedisAuthProvider,
)
from bootstrap.ioc.providers.modules.email import (
    SmtpProvider,
    InfraEmailUseCaseProvider,
)
from bootstrap.ioc.providers.modules.event import (
    MapperEventProvider,
    RuleDomainProvider,
    ServiceDomainEventProvider,
    UseCaseEventProvider,
    ValidatorProvider,
    DmEventProvider,
    RepositoryEventProvider,
    EventProjectionProvider,
)
from bootstrap.ioc.providers.seedwork import (
    TransactionManagerProvider,
    ServiceDomainProvider,
)


DEV_PROVIDERS: list[Provider] = [
    SettingProvider(),
    ElasticSearchProvider(),
    AlchemyProvider(),
    EventBusProvider(),
    FastStreamProvider(),
    RedisProvider(),
    S3ServicesProvider(),
    S3Provider(),
    RulesAuthProvider(),
    RepositoryAuthProvider(),
    MapperAuthProvider(),
    ServiceAuthProvider(),
    UseCaseAuthProvider(),
    DmAlchemyAuthProvider(),
    DmRedisAuthProvider(),
    SmtpProvider(),
    InfraEmailUseCaseProvider(),
    MapperEventProvider(),
    RuleDomainProvider(),
    ServiceDomainEventProvider(),
    UseCaseEventProvider(),
    ValidatorProvider(),
    DmEventProvider(),
    RepositoryEventProvider(),
    EventProjectionProvider(),
    TransactionManagerProvider(),
    ServiceDomainProvider(),
    FastapiProvider(),
]


def get_container() -> AsyncContainer:
    container: AsyncContainer = make_async_container(*DEV_PROVIDERS)

    return container

