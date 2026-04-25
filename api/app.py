from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routers import ingestion, search
from api.dependencies import get_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_factory() # eagerly initialize the factory at startup
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="RAG API",
        description="Retrieval-Augmented Generation API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(ingestion.router)
    app.include_router(search.router)

    return app


app = create_app()