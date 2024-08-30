from promptadmin_server.api.service.ws_manager import WsManager
from fastapi import WebSocket, APIRouter

ws_manager = WsManager()

router = APIRouter()


@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await ws_manager.connect(websocket, token)
