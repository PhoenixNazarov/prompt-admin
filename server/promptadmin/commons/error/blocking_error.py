from .base_error import BaseError


class BlockingError(BaseError):
    def code(self) -> str:
        return 'blocking_error'

    def description(self) -> str:
        return 'Error when try block entity'
