from typing import Any

from settings import SETTINGS
from .router_repository import RouterRepository
from .types import SendableMessage
from ..dto.base_settings import (BaseRouterCredentials, BaseRouter)
from ..dto.broker_message import BrokerMessage
from ..error.init_error import InitError

router_repository = RouterRepository()


class MessageRouter:
    def __init__(self,
                 destination: str,
                 group: str | None = None,
                 credentials: BaseRouterCredentials | None = None,
                 **kwargs):
        self.destination = destination
        if credentials:
            self.router = router_repository.add_router(BaseRouter(name=destination, cred=credentials))
        else:
            self.router = router_repository.get_router(destination)

        if self.router is None:
            raise InitError()

        self.bind_kwargs = kwargs
        if group:
            self.bind_kwargs['group'] = group
        self.bind_kwargs['destination'] = destination

    def _convert_kwargs(self, kwargs: dict[str, Any]):
        copy_bind = self.bind_kwargs.copy()
        copy_bind.update(kwargs)
        return copy_bind

    async def publish(self, message: SendableMessage, user_data: Any = None, **kwargs) -> dict | None:
        broker_message = BrokerMessage(
            data=message,
            destination=self.destination,
            group=kwargs.get('group', self.bind_kwargs['group']),
            departure=SETTINGS.app,
            departure_unique_id=SETTINGS.app_unique_id,
            user_data=user_data,
        )
        return await self.router.publish(broker_message, **self._convert_kwargs(kwargs))

    async def wait_publish(self, message: SendableMessage, user_data: Any = None, **kwargs) -> dict:
        broker_message = BrokerMessage(
            data=message,
            destination=self.destination,
            group=kwargs.get('group', self.bind_kwargs['group']),
            departure=SETTINGS.app,
            departure_unique_id=SETTINGS.app_unique_id,
            user_data=user_data,
        )
        return await self.router.wait_publish(broker_message, **self._convert_kwargs(kwargs))
