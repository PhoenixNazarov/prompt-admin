import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from settings import SETTINGS
from .background_task import BackgroundTask
from ..logging.configure_logstash import configure_loggers


def create_lifespan(background_tasks: list[BackgroundTask] | None = None):
    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        coro_background_tasks = []
        if background_tasks:
            for task in background_tasks:
                coro_background_tasks.append(asyncio.create_task(task.start()))

        yield

        if background_tasks:
            for task in background_tasks:
                await task.stop()
        for coro_task in coro_background_tasks:
            await coro_task

    return app_lifespan


def create_app(
    background_tasks: list[BackgroundTask] = None,
    docs_url: str = None,
    redoc_url: str = None,
    openapi_url: str = None,
) -> FastAPI:
    app_lifespan = create_lifespan(background_tasks)
    app = FastAPI(
        title=SETTINGS.app,
        lifespan=app_lifespan,
        docs_url=docs_url,  # Disable docs (Swagger UI)
        redoc_url=redoc_url,  # Disable redoc
        openapi_url=openapi_url,
    )

    configure_loggers()
    return app
