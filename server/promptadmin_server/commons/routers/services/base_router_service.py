from abc import ABC, abstractmethod

from ...dto.broker_message import BrokerMessage


class BaseRouterService(ABC):
    @abstractmethod
    async def publish(self, message: BrokerMessage, **kwargs) -> dict | None:
        pass

    @abstractmethod
    async def wait_publish(self, message: BrokerMessage, **kwargs) -> dict:
        pass

    @abstractmethod
    async def get_app_lifespan(self, app):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
