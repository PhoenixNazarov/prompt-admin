from .base_error import BaseError


class InitError(BaseError):
    def code(self):
        return 'init_error'

    def description(self):
        return 'Init error'
