import json
from typing import Any

from jinja2.nativetypes import NativeEnvironment
from promptadmin.output.parser_output_service import ParserOutputService
from promptadmin.prompt_service.models import build_model
from promptadmin.prompt_service.models.anthropic import AnthropicModelResponse
from promptadmin.types import ModelServiceInfo, Message
from promptadmin.vars.var_service import VarService

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.dto.prompt_execute import PromptExecute
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.api.service.ws_streamer import WsStreamer
from promptadmin_server.data.entity.input import Input
from promptadmin_server.data.service.input_service import InputService
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService
from settings import SETTINGS


class PreviewTemplateService:
    def __init__(
            self,
            input_service: InputService = None,
            mapping_entity_service: MappingEntityService = None,
            mapping_service: MappingService = None
    ):
        self.input_service = input_service or InputService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()
        self.mapping_service = mapping_service or MappingService()

    async def preview_prompt(self, prompt: Prompt, context: dict[str, str] = None,
                             connection: str | None = None) -> str:
        mapping_entity = await self.mapping_entity_service.find_all()
        if context:
            data = context
        else:
            mapping = await self.mapping_service.find_by_id(prompt.mapping_id)
            current_mapping_entity = [
                i for i in mapping_entity
                if (i.connection_name is None or i.connection_name == mapping.connection_name) and
                   (i.table is None or i.table == mapping.table) and
                   (i.field is None or i.field == mapping.field) and
                   (i.name is None or i.name == prompt.name) and
                   (i.mapping_id is None or i.mapping_id == mapping.id) and
                   (i.entity == 'input')
            ]
            inputs_ids = [i.entity_id for i in current_mapping_entity]
            inputs = await self.input_service.find_by_ids(inputs_ids)

            data = self._collect_context(inputs)
        return await self.preview(prompt.value, data, connection)

    @staticmethod
    async def preview(prompt: str, context: dict[str, Any], connection: str | None = None):
        environment = NativeEnvironment(autoescape=True, enable_async=True)
        template_ = environment.from_string(prompt)

        if connection:
            var_service = VarService(SETTINGS.connections[connection])

            async def render_template(template_key: str, **kwargs):
                templ = await var_service.get_var(template_key)
                templ_ = environment.from_string(templ)
                return await templ_.render_async(
                    **context,
                    **kwargs,
                    render_template=render_template
                )

            return await template_.render_async(
                **context,
                render_template=render_template
            )
        else:
            return await template_.render_async(**context)

    @staticmethod
    async def execute(
            model_service_info: ModelServiceInfo,
            prompt: str,
            history: list[Message],
            parsed_model_type: dict | None,
            user_data: UserData = None,
            uuid: str = None
    ) -> PromptExecute:
        streamer = None
        if user_data and uuid:
            streamer = WsStreamer(user_data.access_token.token, uuid)
        model_response = await build_model(model_service_info).execute(prompt, history, streamer)
        parsed_model_error = False
        if parsed_model_type:
            parsed_model = ParserOutputService().parse_for_json_schema(parsed_model_type, model_response.raw_text)
            if parsed_model is None:
                parsed_model_error = True
            model_response.parsed_model = parsed_model

        return PromptExecute(
            response_model=model_response,
            parsed_model_error=parsed_model_error,
            messages=model_response.messages if isinstance(model_response, AnthropicModelResponse) else []
        )

    @staticmethod
    def _collect_context(inputs: list[Input]):
        data = {}

        def setup(key: str, value):
            dc = data
            for k in key.split('.')[:-1]:
                if k not in dc:
                    dc[k] = {}
                dc = dc[k]
            new_key = key.split('.')[-1]
            dc[new_key] = value

        for i in inputs:
            if i.default_type == 'str':
                setup(i.macro, i.default)
            elif i.default_type == 'json':
                setup(i.macro, json.loads(i.default))
            elif i.default_type == 'bool':
                setup(i.macro, bool(i.default))
            elif i.default_type == 'int':
                setup(i.macro, int(i.default))

        return data
