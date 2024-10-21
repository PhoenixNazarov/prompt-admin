from abc import ABC, abstractmethod


class AbstractStreamer(ABC):
    @abstractmethod
    async def stream(self, text: str):
        pass


class TextStreamer(AbstractStreamer):
    async def stream(self, text: str):
        print(text, end="", flush=True)
