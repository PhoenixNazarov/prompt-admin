import asyncio
import json

from promptadmin.types import ModelServiceInfo, Message
from promptadmin.vars.var_service import VarService

from promptadmin_server.api.service.preview_template_service import PreviewTemplateService
from promptadmin_server.api.service.prompt_load_service import PromptLoadService
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.entity.unit_test import UnitTest
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService
from promptadmin_server.data.service.sync_data_service import SyncDataService
from promptadmin_server.data.service.unit_test_service import UnitTestService
from settings import SETTINGS


class PromptUnitTestService:
    def __init__(
            self,
            preview_template_service: PreviewTemplateService = None,
            sync_data_service: SyncDataService = None,
            prompt_load_service: PromptLoadService = None,
            mapping_service: MappingService = None,
            mapping_entity_service: MappingEntityService = None,
            unit_test_service: UnitTestService = None
    ):
        self.preview_template_service = preview_template_service or PreviewTemplateService()
        self.sync_data_service = sync_data_service or SyncDataService()
        self.prompt_load_service = prompt_load_service or PromptLoadService()
        self.mapping_service = mapping_service or MappingService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()
        self.unit_test_service = unit_test_service or UnitTestService()

    async def process_sync_data(self, sync_data: SyncData, delay: int):
        mapping_entity = await self.mapping_entity_service.find_by_entity_id('sync_data', sync_data.id)
        if len(mapping_entity) <= 0:
            return
        mapping_entity = mapping_entity[0]

        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=Mapping.table, value=mapping_entity.table))
            .filter(ViewParamsFilter(field=Mapping.field, value=mapping_entity.field))
            .filter(ViewParamsFilter(field=Mapping.connection_name, value=mapping_entity.connection_name))
            .build()
        )
        mapping = await self.mapping_service.find_by_view_params_first(view_params)
        if mapping is None:
            return

        if mapping_entity.name:
            await self.process_sync_data_name(sync_data, mapping_entity.name, mapping)
        else:
            prompts = await self.prompt_load_service.load_mapping(mapping)
            for prompt in prompts:
                if prompt.name is None:
                    continue
                await self.process_sync_data_name(sync_data, prompt.name, mapping)
                await asyncio.sleep(delay)

    async def process_sync_data_name(
            self,
            sync_data: SyncData,
            name: str,
            mapping: Mapping,
    ):
        mapping_entity_disable = await self.mapping_entity_service.find_by_prompt_entity(
            mapping.connection_name,
            mapping.table,
            mapping.field,
            name,
            'disable'
        )
        if len(mapping_entity_disable) > 0:
            return
        unit_test = await self.unit_test_service.find_by_sync_data_name(sync_data.id, name)
        if unit_test and unit_test.test_status != 'wait':
            return
        if unit_test is None:
            unit_test = UnitTest(
                sync_data_id=sync_data.id,
                name=name
            )
        await self.process(unit_test, sync_data, mapping)

    async def process(self, unit_test: UnitTest, sync_data: SyncData, mapping: Mapping):
        unit_test.test_status = 'process'
        unit_test.test_exception = None
        unit_test.test_preview = None
        unit_test.test_response_model = None
        unit_test = await self.unit_test_service.save(unit_test)

        await self.preview(unit_test, sync_data, mapping)
        if unit_test.test_exception:
            return
        await self.execution(unit_test, sync_data)
        if unit_test.test_exception:
            return

    async def preview(self, unit_test: UnitTest, sync_data: SyncData, mapping: Mapping):
        unit_test.test_status = 'preview'
        try:
            connection = SETTINGS.connections.get(mapping.connection_name)
            if connection is None:
                return {}
            collect_vars = await VarService(connection).collect_vars()

            context = {}
            context.update({'var': collect_vars})
            context.update(json.loads(sync_data.template_context_default))

            prompt = await self.prompt_load_service.load_mapping_name(mapping, unit_test.name)
            preview = self.preview_template_service.preview(prompt, context)
            unit_test.test_preview = preview
        except Exception as e:
            unit_test.test_exception = str(e)
        await self.unit_test_service.save(unit_test)

    async def execution(self, unit_test: UnitTest, sync_data: SyncData):
        unit_test.test_status = 'execution'
        try:
            execution = await self.preview_template_service.execute(
                model_service_info=ModelServiceInfo.model_validate_json(sync_data.service_model_info),
                prompt=unit_test.test_preview,
                history=[Message.model_validate(i) for i in json.loads(sync_data.history_context_default)],
                parsed_model_type=json.loads(sync_data.parsed_model_type) if sync_data.parsed_model_type else None
            )
            unit_test.test_response_model = execution.response_model.json()
            if execution.parsed_model_error:
                unit_test.test_exception = 'Parsed model error'
        except Exception as e:
            unit_test.test_exception = str(e)
        await self.unit_test_service.save(unit_test)
