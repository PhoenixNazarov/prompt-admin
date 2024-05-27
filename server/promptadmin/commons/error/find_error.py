from .base_error import BaseError


class FindError(BaseError):
    def code(self) -> str:
        return 'find_error'

    def description(self) -> str:
        return 'Error when find in services/repositories'
