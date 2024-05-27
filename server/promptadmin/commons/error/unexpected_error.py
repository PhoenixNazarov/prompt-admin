from .base_error import BaseError


class UnexpectedError(BaseError):
    def code(self):
        return 'unexpected_error'

    def description(self):
        return 'Undefined error'
