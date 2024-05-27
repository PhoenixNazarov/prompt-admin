from ..entity.account import Account
from ...commons.repository import AsyncBaseRepository


class AccountRepository(AsyncBaseRepository[Account]):
    def __init__(self):
        super().__init__(Account)
