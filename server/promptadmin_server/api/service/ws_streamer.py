from promptadmin.prompt_service.models.abstract_streamer import AbstractStreamer

from promptadmin_server.api.dto.ws.promt_execute_response import PromptExecuteResponse
from promptadmin_server.api.service.ws_manager import WsManager


class WsStreamer(AbstractStreamer):
    def __init__(
            self,
            access_token: str,
            uuid: str,
            ws_manager: WsManager = None,
    ):
        self.access_token = access_token
        self.uuid = uuid
        self.ws_manager = ws_manager or WsManager()

    async def stream(self, text: str):
        response = PromptExecuteResponse(text=text, uuid=self.uuid)
        await self.ws_manager.send_to_access_token(self.access_token, response)
