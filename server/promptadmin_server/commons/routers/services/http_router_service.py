import asyncio
from asyncio import Task

from httpx import AsyncClient, Response
import logging

from .base_router_service import BaseRouterService
from ...dto.base_settings import RouterHttpCred

from ...dto.broker_message import BrokerMessage

logger = logging.getLogger(__name__)


class HttpRouterService(BaseRouterService):
    def __init__(self, cred: RouterHttpCred):
        self.cred = cred
        self.headers = {
            'Token': cred.token
        }
        self.base_url = self.cred.host.removesuffix('/')
        if self.cred.port:
            self.base_url += f':{self.cred.port}'

    async def publish(self, message: BrokerMessage, **kwargs) -> None:
        try:
            asyncio.create_task(self._request(message, **kwargs)).add_done_callback(self._publish_callback_wrap)
        except Exception as e:
            logger.error('Error when send message', extra={'broker-message': message, 'broker-args': kwargs},
                         exc_info=e)
            raise e

    @staticmethod
    def _publish_callback_wrap(task: Task):
        if task.exception():
            logger.error('Exception on publish http', exc_info=task.exception())
        if task.cancelled() or not task.done():
            logger.error('Exception on publish http')
        res: Response = task.result()
        if res.status_code != 200:
            logger.error(
                'Error on http request',
                extra={'text': res.text, 'status_code': res.status_code, 'url': res.url}
            )

    async def _request(
            self,
            message: BrokerMessage,
            destination: str,
            group: str,
            wait_timeout: int = 60,
            headers: dict[str, str | int] | None = None
    ) -> Response:
        async with AsyncClient(headers=self.headers, base_url=self.base_url) as client:
            return (
                await client.post(
                    group,
                    timeout=wait_timeout,
                    json=message.model_dump(mode='json'),
                    headers=headers
                )
            )

    async def wait_publish(self, message: BrokerMessage, **kwargs) -> dict:
        try:
            res = await self._request(message, **kwargs)
        except Exception as e:
            logger.error('Error when send message', extra={'broker-message': message, 'kwargs': kwargs}, exc_info=e)
            raise e

        if res.status_code != 200:
            logger.error(
                'Error on http request',
                extra={'text': res.text, 'status_code': res.status_code, 'url': res.url}
            )
            raise ValueError()
        return res.json()

    async def get_app_lifespan(self, app):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
