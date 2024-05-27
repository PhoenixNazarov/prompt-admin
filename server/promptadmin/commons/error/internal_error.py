from .base_error import BaseError


class InternalError(BaseError):
    def code(self) -> str:
        return 'internal_error'

    def description(self) -> str:
        return 'Internal error'
