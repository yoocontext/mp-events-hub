import asyncio
import json
from pathlib import Path

from elasticsearch import AsyncElasticsearch

from bootstrap.ioc import get_container


async def ensure_index(
    index_name: str,
    index_body: dict,
    elc: AsyncElasticsearch,
) -> None:
    exists = await elc.indices.exists(index=index_name)

    if exists:
        print(f"Индекс '{index_name}' уже существует, пропускаем создание.")
        return

    await elc.indices.create(index=index_name, body=index_body)
    print(f"Индекс '{index_name}' успешно создан.")


INDICES_DIR = f"{Path(__file__).parent}/indices"

async def create_indices() -> None:
    container = get_container()

    async with container() as cont:
        elc: AsyncElasticsearch = await cont.get(AsyncElasticsearch)

        with open(f"{INDICES_DIR}/event.json", mode="r", encoding="utf-8") as f:
            event_index: dict = json.load(f)

            await ensure_index(
                index_name="events.events",
                index_body=event_index,
                elc=elc,
            )

if __name__ == "__main__":
    asyncio.run(create_indices())