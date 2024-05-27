from ..entity.access_token import AccessToken
from ..repository.access_token_repository import AccessTokenRepository
from ...commons.service import AsyncBaseService


class AccessTokenService(AsyncBaseService[AccessToken]):
    def __init__(self, repository: AccessTokenRepository = None):
        super().__init__(repository or AccessTokenRepository())
