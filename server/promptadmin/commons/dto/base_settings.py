import os
import time
from typing import Optional, Literal, Union, TypeAlias
from enum import StrEnum

from pydantic import BaseModel, Field


class BaseSettingsLogstash(BaseModel):
    host: Optional[str] = os.getenv('LOGSTASH_HOST')
    port: Optional[int] = int(os.getenv('LOGSTASH_PORT', 0))
    username: Optional[str] = os.getenv('LOGSTASH_USERNAME')
    password: Optional[str] = os.getenv('LOGSTASH_PASSWORD')
    environment: Optional[str] = os.getenv('LOGSTASH_ENVIRONMENT')

    # Logger and set source
    system_loggers: dict[str, str] = {
        'src': 'src',
        'catalyst': 'ctl-lib',
        # 'fastapi': 'fastapi', individual change
        'uvicorn': 'uvicorn',
    }

    config_loggers: dict[str, str] = {

    }


class RouterRabbitmqBrokerCred(BaseModel):
    # Routers are formed into one group with one cred
    cred: Optional[str] = None
    group: Optional[str] = 'default-rabbitmq'
    max_consumers: int | None = None


class RouterRedisBrokerCred(BaseModel):
    # Routers are formed into one group with one cred
    cred: Optional[str] = None
    group: Optional[str] = 'default-redis'


class RouterHttpCred(BaseModel):
    host: str | None = None
    port: int | None = None
    token: str | None = None


BaseRouterCredentials: TypeAlias = RouterRabbitmqBrokerCred | RouterRedisBrokerCred | RouterHttpCred


class BaseRouter(BaseModel):
    name: str
    cred: BaseRouterCredentials


class DatabaseCred(BaseModel):
    database_prefix: str = ''  # empty as default

    async_: bool = True
    dialect: str = 'postgresql'
    driver: str | None = 'asyncpg'

    username: str
    password: str
    host: str
    port: int
    database: str


class RedisCacheCred(BaseModel):
    host: str
    port: int
    password: str | None = None


class BaseSettings(BaseModel):
    # Microservice name
    app: str
    # Microservice unique id
    app_unique_id: int = Field(default_factory=lambda: int(time.time() * 1000))

    # Addresses for databases. SqlController
    # For each microservice you can specify its own address.
    database: list[DatabaseCred] = []

    # Redis database cache
    redis_cache: RedisCacheCred | None = None

    # For default rabbitmq or redis. Create instance with group "default-rabbitmq" or "default-redis"
    message_routers: list[BaseRouter] = []

    # The microservice will run on this host and this port
    host: str = '0.0.0.0'
    port: int = 8080

    # If the application accepts requests directly from the user.
    # This field must be specified to decrypt the user session
    # The code for this is in the package um
    session_secret: Optional[str] = None

    logstash_logger: Optional[BaseSettingsLogstash] = BaseSettingsLogstash()
