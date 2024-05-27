from faststream.redis.fastapi import RedisRouter
from .base_router_service import BaseRouterService
from ...dto.base_settings import RouterRedisBrokerCred
import logging

from ...dto.broker_message import BrokerMessage

logger = logging.getLogger(__name__)


class RedisRouterService(BaseRouterService):
    def __init__(self, cred: RouterRedisBrokerCred):
        self.cred = cred
        host = cred.cred.split('//')[1].split(':')[0]
        # password = v.removeprefix('redis:').split('//')[0]
        self.router = RedisRouter(url=cred.cred, host=host)

    async def publish(self, message: BrokerMessage, **kwargs) -> None:
        try:
            return await self._publish(message, **kwargs)
        except Exception as e:
            logger.error('Error when send message', extra={'broker-message': message, 'broker-args': kwargs},
                         exc_info=e)
            raise e

    async def _publish(
            self,
            message: BrokerMessage,
            destination: str,
            group: str
    ):
        if group != '':
            channel = f'{destination}.{group}'
        else:
            channel = destination
        await self.router.broker.publish(message, channel)

    async def wait_publish(self, message: BrokerMessage, **kwargs) -> dict:
        raise NotImplementedError()

    async def get_app_lifespan(self, app):
        return self.router.lifespan_context(app)

    async def __aenter__(self):
        await self.router.broker.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.router.broker.__aexit__(exc_type, exc_val, exc_tb)
