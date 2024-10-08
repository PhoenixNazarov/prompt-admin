import os
from promptadmin_server.commons.dto.base_settings import (
    BaseSettings,
    BaseRouter,
    DatabaseCred
)

from promptadmin.types import Settings


class _Settings(BaseSettings, Settings):
    app: str = 'prompt-admin'

    database: list[DatabaseCred] = [
        DatabaseCred(
            username=os.environ['PA_DATABASE_USERNAME'],
            password=os.environ['PA_DATABASE_PASSWORD'],
            host=os.environ['PA_DATABASE_HOST'],
            port=int(os.environ['PA_DATABASE_PORT']),
            database=os.environ['PA_DATABASE_DATABASE']
        )
    ]

    message_routers: list[BaseRouter] = []

    connections: dict[str, str] = {}

    sync_edpoints: dict[str, str] = {}
    sync_secrets: dict[str, str] = {}


SETTINGS = _Settings()

for k, v in os.environ.items():
    if k.startswith('PA_CONNECTION_'):
        name = k.removeprefix('PA_CONNECTION_').lower()
        SETTINGS.connections[name] = v

for k, v in os.environ.items():
    if k.startswith('PA_SYNC_ENDPOINT_'):
        name = k.removeprefix('PA_SYNC_ENDPOINT_').lower()
        SETTINGS.sync_edpoints[name] = v

for k, v in os.environ.items():
    if k.startswith('PA_SYNC_SECRET_'):
        name = k.removeprefix('PA_SYNC_SECRET_').lower()
        SETTINGS.sync_secrets[name] = v
