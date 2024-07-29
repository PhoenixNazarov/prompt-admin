import json

import jinja2

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.data.entity.input import Input
from promptadmin_server.data.service.input_service import InputService
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService


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

    async def preview_prompt(self, prompt: Prompt, context: dict[str, str] = None) -> str:
        mapping_entity = await self.mapping_entity_service.find_all()
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

        data = context or self._collect_context(inputs)
        print(data)
        environment = jinja2.Environment()
        template = environment.from_string(prompt.value)

        return template.render(**data)

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
