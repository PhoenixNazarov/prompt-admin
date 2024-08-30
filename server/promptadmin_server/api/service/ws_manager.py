import cachetools
from fastapi import WebSocket, WebSocketDisconnect

from promptadmin_server.api.dto.ws.base_ws_response import BaseWsResponse
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.commons.singleton_metaclass import Singleton

from promptadmin_server.data.entity.access_token import get_random_string


class WsManager(metaclass=Singleton):
    def __init__(self):
        self._auth_tokens = cachetools.TTLCache(maxsize=128, ttl=1 * 60)
        self._connections: dict[str, list[WebSocket]] = {}

    async def generate_auth_token(self, user_data: UserData) -> str:
        token = get_random_string(45)
        self._auth_tokens[token] = user_data.access_token.token
        return token

    async def connect(self, websocket: WebSocket, token: str):
        if token not in self._auth_tokens:
            raise ValueError()
        access_token = self._auth_tokens.pop(token)
        if access_token not in self._connections:
            self._connections[access_token] = []
        self._connections[access_token].append(websocket)
        await websocket.accept()
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        except RuntimeError:
            pass
        finally:
            self._connections[access_token].remove(websocket)
            if len(self._connections[access_token]) <= 0:
                self._connections.pop(access_token)

    async def send_to_access_token(self, token: str, response: BaseWsResponse):
        websockets = self._connections.get(token)
        if websockets is None:
            return
        for websocket in websockets:
            await websocket.send_json(response.model_dump_json())
