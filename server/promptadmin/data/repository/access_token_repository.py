from ..entity.access_token import AccessToken
from ...commons.repository import AsyncBaseRepository


class AccessTokenRepository(AsyncBaseRepository[AccessToken]):
    def __init__(self):
        super().__init__(AccessToken)
