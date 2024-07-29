import base64
import hashlib
import json

from itsdangerous import TimestampSigner, BadSignature
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.requests import HTTPConnection

from promptadmin_server.api.service.user_manager_service import UserManagerService


class SessionMiddleware:
    def __init__(self,
                 app: ASGIApp,
                 secret_key: str,
                 session_cookie: str = 'session'):
        self.app = app
        self.path = '/'
        self.security_flags = 'HttpOnly;'
        self.signer = TimestampSigner(secret_key, salt='cookie-session', digest_method=hashlib.sha1,
                                      key_derivation='hmac')
        self.session_cookie = session_cookie
        self.user_manager_service = UserManagerService()
        self.max_age = 259200

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] not in ('http', 'websocket'):  # pragma: no cover
            await self.app(scope, receive, send)
            return
        connection = HTTPConnection(scope)

        token = ''
        initial_session_was_empty = True
        if self.session_cookie in connection.cookies:
            data = connection.cookies[self.session_cookie].encode('utf-8')
            try:
                data = self.signer.unsign(data, max_age=None)
                session = json.loads(base64.urlsafe_b64decode(data))
                token = session.get('token')
                initial_session_was_empty = False
            except BadSignature:
                token = ''
            except json.JSONDecodeError:
                token = ''
            except AttributeError:
                token = ''

        user_data = await self.user_manager_service.load_user_data(token)
        scope['user_data'] = user_data
        scope['session'] = {'token': user_data.access_token.token}

        async def send_wrapper(message: Message) -> None:
            if message['type'] == 'http.response.start':
                if scope['session']:
                    # We have session data to persist.
                    data = base64.b64encode(json.dumps(scope['session']).encode('utf-8'))
                    data = self.signer.sign(data)
                    headers = MutableHeaders(scope=message)
                    header_value = '{session_cookie}={data}; path={path}; {max_age}{security_flags}'.format(
                        # noqa E501
                        session_cookie=self.session_cookie,
                        data=data.decode('utf-8'),
                        path=self.path,
                        max_age=f'Max-Age={self.max_age}; ' if self.max_age else '',
                        security_flags=self.security_flags,
                    )
                    headers.append('Set-Cookie', header_value)
                elif not initial_session_was_empty:
                    # The session has been cleared.
                    headers = MutableHeaders(scope=message)
                    header_value = '{session_cookie}={data}; Path={path}; {expires}{security_flags}'.format(
                        # noqa E501
                        session_cookie=self.session_cookie,
                        data='null',
                        path=self.path,
                        expires='expires=Thu, 01 Jan 1970 00:00:00 GMT; ',
                        security_flags=self.security_flags,
                    )
                    headers.append('Set-Cookie', header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)
