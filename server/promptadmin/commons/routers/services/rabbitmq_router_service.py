from faststream.rabbit import RabbitExchange, RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter

from .base_router_service import BaseRouterService
from .rabbit_wait_block import RabbitWaitBlock
from ...dto.base_settings import RouterRabbitmqBrokerCred
from ...dto.broker_message import BrokerMessage
from .. import consts

import logging

logger = logging.getLogger(__name__)


class RabbitmqRouterService(BaseRouterService):
    def __init__(self, cred: RouterRabbitmqBrokerCred):
        self.cred = cred
        self.router = RabbitRouter(cred.cred, max_consumers=cred.max_consumers)
        self.rabbit_wait_block = RabbitWaitBlock()

    async def publish(self, message: BrokerMessage, **kwargs) -> dict | None:
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
            group: str,
            durable: bool = True,
            exclusive: bool = False,
            ref_format: bool = True,
            destination_index: int | None = None,
            wait_timeout: int = 60,
            wait: bool = False,
            priority: int | None = None,
    ) -> dict | None:
        if ref_format:
            exchange = RabbitExchange(name=consts.exchange(destination), durable=durable)
            if destination_index:
                queue = RabbitQueue(name=consts.index_queue(destination, destination_index, group),
                                    durable=durable, exclusive=exclusive)
            else:
                queue = RabbitQueue(name=consts.queue(destination, group), durable=durable, exclusive=exclusive)
        else:
            exchange = RabbitExchange(name=destination, durable=durable)
            queue = RabbitQueue(name=group, durable=durable, exclusive=exclusive)
        message.reply_response = wait
        await self.router.broker.publish(
            message,
            queue,
            exchange,
            expiration=wait_timeout,
            priority=priority
        )
        if wait:
            return await self.rabbit_wait_block.register_wait_response(message.message_id, wait_timeout)

    async def wait_publish(self, message: BrokerMessage, **kwargs) -> dict:
        return await self.publish(message, wait=True, **kwargs)

    async def get_app_lifespan(self, app):
        return self.router.lifespan_context(app)

    async def __aenter__(self):
        await self.router.broker.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.router.broker.__aexit__(exc_type, exc_val, exc_tb)
