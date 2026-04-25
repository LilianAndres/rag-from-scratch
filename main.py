import asyncio

from app.config.app_settings import AppSettings
from app.src.core.search.search_query import SearchQuery
from app.src.factories import ApplicationFactory


async def run() -> None:
    settings = AppSettings()
    factory = ApplicationFactory(settings)

    ingestion = factory.create_ingestion_pipeline()
    await ingestion.ingest(["file://sample.pdf"])
    print("Ingestion complete.")

    rag = factory.create_rag_pipeline()
    query = SearchQuery(text="How does scaled dot-product attention work?")
    result = await rag.run(query)

    print(f"\nAnswer:\n{result.answer}")
    print(f"\nSources ({len(result.sources)}):")
    for i, source in enumerate(result.sources, 1):
        score = f"{source.score:.3f}" if source.score is not None else "n/a"
        print(f"  [{i}] (score: {score}) {source.chunk.content[:120]}...")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()