from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from elasticsearch import AsyncElasticsearch

from bootstrap.settings import Settings


class ElasticSearchProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_elc(
        self,
        settings: Settings,
    ) -> AsyncIterable[AsyncElasticsearch]:

        async with AsyncElasticsearch(
            hosts=[settings.elastic.host],
        ) as elc:
            yield elc