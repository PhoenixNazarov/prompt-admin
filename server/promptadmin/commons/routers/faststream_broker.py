import functools
import logging
from faststream.rabbit import RabbitExchange, RabbitQueue

from settings import SETTINGS
from .router_repository import RouterRepository
from .services import (
    RabbitmqRouterService,
    RedisRouterService
)
from .services.rabbit_wait_block import RabbitWaitBlock
from ..dto.broker_message import BrokerMessage, BrokerResponse
from ..error.init_error import InitError
from ..error.unexpected_error import UnexpectedError
from ..singleton_metaclass import Singleton
from . import consts

logger = logging.getLogger(__name__)


class FastStreamBroker(metaclass=Singleton):
    def __init__(self, name: str):
        self.name = name
        self.router_repository = RouterRepository()
        self.router_service = self.router_repository.get_router(name)
        if isinstance(self.router_service, RabbitmqRouterService):
            self.router = self.router_service.router
            self.init_response_queue()
        elif isinstance(self.router_service, RedisRouterService):
            self.router = self.router_service.router
        else:
            raise InitError()

    def get_router(self):
        return self.router

    def init_response_queue(self):
        rabbit_wait_block = RabbitWaitBlock()

        async def response_handler(message: BrokerMessage[BrokerResponse]):
            rabbit_wait_block.do_response(message.data.reply_message_id, message.data.data)

        exchange = RabbitExchange(consts.exchange(self.name), durable=True)
        queue = RabbitQueue(consts.index_queue(self.name, SETTINGS.app_unique_id, consts.RESPONSE_QUEUE),
                            exclusive=True)
        self.router.subscriber(queue, exchange)(response_handler)

    def subscriber(self, name: str, max_priority: int = None):
        if isinstance(self.router_service, RedisRouterService):
            def subscriber_wrap(func):
                return self.router.subscriber(f'{self.name}.{name}')(func)

            return subscriber_wrap
        elif isinstance(self.router_service, RabbitmqRouterService):
            exchange = RabbitExchange(consts.exchange(self.name), durable=True)

            arguments = {}
            if max_priority:
                arguments.update({'x-max-priority': max_priority})

            queue = RabbitQueue(consts.queue(self.name, name), durable=True, arguments=arguments)

            def func_with_response(func):
                @functools.wraps(func)
                async def wrapper(*args, **kwargs):
                    result = await func(*args, **kwargs)
                    message = kwargs.get('message')
                    if message:
                        message = dict(message)
                        if message['reply_response']:
                            destination = message['departure']
                            group = consts.RESPONSE_QUEUE
                            broker_message = BrokerMessage(
                                data=BrokerResponse(reply_message_id=message['message_id'], data=result),
                                destination=destination,
                                group=group,
                                departure=SETTINGS.app,
                                departure_unique_id=SETTINGS.app_unique_id
                            )
                            router_service = self.router_repository.get_router(destination)
                            if router_service is None:
                                router_service = self.router_repository.get_router_by_group('default-rabbitmq')
                            if router_service is None:
                                logger.error('Cant send async response message to rabbitmq',
                                             extra={'destination': destination, 'group': group})
                                raise UnexpectedError()
                            if isinstance(router_service, RabbitmqRouterService):
                                await router_service.publish(
                                    broker_message,
                                    destination=destination,
                                    group=group,
                                    exclusive=True,
                                    destination_index=message['departure_unique_id']
                                )
                            else:
                                raise UnexpectedError()
                    return result

                return wrapper

            def subscriber_wrap(func):
                return self.router.subscriber(queue, exchange)(func_with_response(func))

            return subscriber_wrap
        else:
            raise InitError()
