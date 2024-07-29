import asyncio
from asyncio import Queue

from pydantic import BaseModel

from ...error.internal_error import InternalError
from ...singleton_metaclass import Singleton


class Response(BaseModel):
    message: dict
    exception: bool = False


class RabbitWaitBlock(metaclass=Singleton):
    def __init__(self):
        self.queues: dict[str, Queue[Response]] = {}

    async def register_wait_response(self, message_id: str, timeout: int) -> dict:
        message_uid = message_id
        queue = Queue(maxsize=1)
        self.queues[message_id] = queue
        try:
            response = await asyncio.wait_for(queue.get(), timeout=timeout)
            if response.exception:
                raise InternalError()
            return response.message
        except asyncio.TimeoutError as e:
            raise TimeoutError() from e
        finally:
            if message_uid in self.queues:
                self.queues.pop(message_uid)

    def _set_response(self, message_id: str, response: Response):
        queue = self.queues.pop(message_id)
        if not queue:
            return

        try:
            queue.put_nowait(response)
        except asyncio.QueueFull:
            return

    def do_response(self, message_id: str, response: dict):
        self._set_response(message_id, Response(message=response))

    def do_exception(self, message_id: str):
        self._set_response(message_id, Response(message={}, exception=True))
