from abc import ABC, abstractmethod


class BackgroundTask(ABC):
    @abstractmethod
    async def start(self):
        """
        Method for start operation in starlette lifespan
        """

    @abstractmethod
    async def stop(self):
        """
        Method for stop operation in starlette lifespan
        """
