from promptadmin_server.api.dto.ws.base_ws_response import BaseWsResponse


class PromptExecuteResponse(BaseWsResponse):
    type: str = 'prompt-execute'

    uuid: str
    text: str

