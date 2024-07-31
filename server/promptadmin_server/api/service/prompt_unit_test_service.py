import json

from promptadmin.types import ModelServiceInfo, Message
from promptadmin.vars.var_service import VarService

from promptadmin_server.api.service.preview_template_service import PreviewTemplateService
from promptadmin_server.api.service.prompt_load_service import PromptLoadService
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService
from promptadmin_server.data.service.sync_data_service import SyncDataService
from settings import SETTINGS


class PromptUnitTestService:
    def __init__(
            self,
            preview_template_service: PreviewTemplateService = None,
            sync_data_service: SyncDataService = None,
            prompt_load_service: PromptLoadService = None,
            mapping_service: MappingService = None,
            mapping_entity_service: MappingEntityService = None
    ):
        self.preview_template_service = preview_template_service or PreviewTemplateService()
        self.sync_data_service = sync_data_service or SyncDataService()
        self.prompt_load_service = prompt_load_service or PromptLoadService()
        self.mapping_service = mapping_service or MappingService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()

    async def process(self, sync_data: SyncData):
        # sync_data
        sync_data.test_status = 'process'
        sync_data.test_exception = None
        sync_data.test_preview = None
        sync_data.test_response_model = None
        sync_data = await self.sync_data_service.save(sync_data)

        await self.preview(sync_data)
        if sync_data.test_exception:
            return
        await self.execution(sync_data)
        if sync_data.test_exception:
            return

    async def preview(self, sync_data: SyncData):
        sync_data.test_status = 'preview'
        try:
            view_params = (
                ViewParamsBuilder()
                .filter(ViewParamsFilter(field=MappingEntity.entity, value='sync_data'))
                .filter(ViewParamsFilter(field=MappingEntity.entity_id, value=sync_data.id))
                .build()
            )
            mapping_entity = await self.mapping_entity_service.find_by_view_params_first(view_params)
            view_params = (
                ViewParamsBuilder()
                .filter(ViewParamsFilter(field=Mapping.table, value=mapping_entity.table))
                .filter(ViewParamsFilter(field=Mapping.field, value=mapping_entity.field))
                .filter(ViewParamsFilter(field=Mapping.connection_name, value=mapping_entity.connection_name))
                .build()
            )
            mapping = await self.mapping_service.find_by_view_params_first(view_params)

            connection = SETTINGS.connections.get(mapping.connection_name)
            if connection is None:
                return {}
            collect_vars = await VarService(connection).collect_vars()

            context = {}
            context.update(collect_vars)
            context.update(json.loads(sync_data.template_context_default))

            prompt = await self.prompt_load_service.load(mapping, mapping_entity.name)
            preview = self.preview_template_service.preview(prompt, context)
            sync_data.test_preview = preview
        except Exception as e:
            sync_data.test_exception = str(e)
        await self.sync_data_service.save(sync_data)

    async def execution(self, sync_data: SyncData):
        sync_data.test_status = 'execution'
        try:
            execution = await self.preview_template_service.execute(
                model_service_info=ModelServiceInfo.model_validate_json(sync_data.service_model_info),
                prompt=sync_data.test_preview,
                history=[Message.model_validate(i) for i in json.loads(sync_data.history_context_default)],
                parsed_model_type=json.loads(sync_data.parsed_model_type) if sync_data.parsed_model_type else None
            )
            sync_data.test_response_model = execution.response_model.json()
            if execution.parsed_model_error:
                sync_data.test_exception = 'Parsed model error'
        except Exception as e:
            sync_data.test_exception = str(e)
        await self.sync_data_service.save(sync_data)
