from abc import ABC, abstractmethod

from .schedule import sleep_schedule


class BaseJob(ABC):
    @abstractmethod
    def delay(self) -> int:
        pass

    @abstractmethod
    def process_task(self):
        pass

    def polling(self):
        sleep_schedule(self.process_task, self.delay())
