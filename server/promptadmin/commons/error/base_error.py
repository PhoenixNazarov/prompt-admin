from abc import ABC, abstractmethod


class BaseError(Exception, ABC):
    def __init__(self, message=''):
        super().__init__()
        self.message = message

    @abstractmethod
    def code(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass
