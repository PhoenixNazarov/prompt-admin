import logging
from typing import Optional

from settings import SETTINGS
from ..error.init_error import InitError

from ..singleton_metaclass import Singleton
from ..dto.base_settings import RouterRedisBrokerCred
from ..dto.base_settings import RouterRabbitmqBrokerCred
from ..dto.base_settings import RouterHttpCred
from ..dto.base_settings import BaseRouter
from .services.base_router_service import BaseRouterService

from .services.rabbitmq_router_service import RabbitmqRouterService
from .services.redis_router_service import RedisRouterService
from .services.http_router_service import HttpRouterService

logger = logging.getLogger()


class RouterRepository(metaclass=Singleton):
    def __init__(self):
        self._name_routers: dict[str, BaseRouterService] = {}
        self._group_routers: dict[str, BaseRouterService] = {}

        self._aenter_routers = []
        self.init_settings_router()

    def init_settings_router(self):
        for i in SETTINGS.message_routers:
            self.add_router(i)

    @staticmethod
    def _check_router_cred(
            name: str,
            cred: Optional[str],
            router: BaseRouterService,
            router_instance: type[RabbitmqRouterService | RedisRouterService]
    ):
        if isinstance(router, router_instance):
            if cred is not None and router.cred.cred != cred:
                logger.error(f'Find incorrect credentials. {name} data conflict with exiting router credentials')
                raise InitError()
        else:
            logger.error(f'Already instance for ${name} is different, need rabbitmq')
            raise InitError()

    def _add_broker_router(
            self,
            name: str,
            group: str,
            router_cred: RouterRedisBrokerCred | RouterRabbitmqBrokerCred,
            broker_type: type[RabbitmqRouterService | RedisRouterService],
            default_group: str
    ):
        cred = router_cred.cred

        # 1. If name already set
        if name in self._name_routers:
            router = self._name_routers[name]
            # 2. Check router correct
            self._check_router_cred(name, cred, router, broker_type)

        # 3. default -> make default group
        # 4. if cred and group are not set, take a default group
        elif group is None and cred is None:
            if default_group not in self._group_routers:
                logger.error(f'Credentials for ${name} not set and default router not exist')
                raise InitError()
            self._name_routers[name] = self._group_routers[default_group]

        # 5. exist router
        elif group is not None:
            # 6. group exist
            if group in self._group_routers:
                router = self._group_routers[group]
                self._check_router_cred(name, cred, router, broker_type)
                self._name_routers[name] = self._group_routers[default_group]
            # 7. create group
            else:
                if cred is None:
                    logger.error(f'Credentials for ${name} not set and default router not exist')
                    raise InitError()
                router = broker_type(router_cred)
                self._group_routers[group] = router
                self._name_routers[name] = router

        # 8. create a router without a group
        elif cred is not None:
            self._name_routers[name] = broker_type(router_cred)

        else:
            logger.error(f'Can not attach any router or create router for {name}')
            raise InitError()

    def add_router(self, router_data: BaseRouter) -> BaseRouterService:
        name = router_data.name
        if isinstance(router_data.cred, RouterRabbitmqBrokerCred):
            self._add_broker_router(name, router_data.cred.group, router_data.cred, RabbitmqRouterService,
                                    'default-rabbitmq')

        elif isinstance(router_data.cred, RouterRedisBrokerCred):
            self._add_broker_router(name, router_data.cred.group, router_data.cred, RedisRouterService,
                                    'default-redis')

        elif isinstance(router_data.cred, RouterHttpCred):
            token = router_data.cred.token
            port = router_data.cred.port
            host = router_data.cred.host

            if name in self._name_routers:
                router = self._name_routers[name]
                if not isinstance(router, HttpRouterService):
                    logger.error(f'Already instance for ${name} is different, need http')
                    raise InitError()
                if (token is not None and router.cred.token != token) or \
                        (host is not None and router.cred.host != host) or \
                        (port is not None and router.cred.port != port):
                    logger.error(f'Already instance credentials for ${name} is different')
                    raise InitError()
            else:
                self._name_routers[name] = HttpRouterService(router_data.cred)
        else:
            raise InitError('Cant process router_data.cred type')

        return self._name_routers[name]

    def get_router(self, name: str) -> BaseRouterService | None:
        return self._name_routers.get(name)

    def get_router_by_group(self, name: str) -> BaseRouterService:
        return self._group_routers.get(name)

    async def get_app_lifespans(self, app):
        unique_routers = []
        for i in list(self._group_routers.values()) + list(self._name_routers.values()):
            if i not in unique_routers:
                unique_routers.append(i)

        self._aenter_routers = unique_routers
        res = []
        for router in unique_routers:
            lifespan = await router.get_app_lifespan(app)
            if lifespan:
                res.append(lifespan)
        return res

    async def __aenter__(self):
        unique_routers = []
        for i in list(self._group_routers.values()) + list(self._name_routers.values()):
            if i not in unique_routers:
                unique_routers.append(i)

        self._aenter_routers = unique_routers
        for i in unique_routers:
            await i.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for i in self._aenter_routers:
            await i.__aexit__(exc_type, exc_val, exc_tb)
