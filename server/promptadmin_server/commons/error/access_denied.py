from .base_error import BaseError


class AccessDenied(BaseError):
    def code(self):
        return 'access_denied'

    def description(self):
        return 'Error when a user accesses an Object to which he does not have access'
