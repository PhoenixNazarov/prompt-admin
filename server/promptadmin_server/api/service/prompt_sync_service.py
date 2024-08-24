import json
import logging

import httpx

from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService
from promptadmin_server.data.service.sync_data_service import SyncDataService

logger = logging.getLogger(__name__)


class PromptSyncService:
    def __init__(
            self,
            mapping_service: MappingService = None,
            sync_data_service: SyncDataService = None,
            mapping_entity_service: MappingEntityService = None
    ):
        self.mapping_service = mapping_service or MappingService()
        self.sync_data_service = sync_data_service or SyncDataService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()

    async def sync_endpoint(self, endpoint: str, secret: str):
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(endpoint, headers={'Prompt-Admin-Secret': secret})
                await self.sync_json(r.json())
            except Exception as e:
                logger.error('Sync exception', exc_info=e)

    async def sync_json(self, result: dict):
        app = result['app']
        prompt_service_info = result['prompt_service_info']
        for i in prompt_service_info:
            await self.sync(
                app=app,
                table=i['table'],
                field=i['field'],
                field_name=i['field_name'],
                name=i['name'],
                service_model_info=i['service_model_info'],
                template_context_type=i['template_context_type'],
                template_context_default=i['template_context_default'],
                history_context_default=i['history_context_default'],
                parsed_model_type=i['parsed_model_type'],
                parsed_model_default=i['parsed_model_default'],
                fail_parse_model_strategy=i['fail_parse_model_strategy']
            )

    async def sync(
            self,
            app: str,
            table: str,
            field: str,
            field_name: str,
            name: str | None,
            service_model_info: dict,
            template_context_type: dict,
            template_context_default: dict,
            history_context_default: list,
            parsed_model_type: dict | None,
            parsed_model_default: dict | None,
            fail_parse_model_strategy: str | None
    ):
        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=Mapping.table, value=table))
            .filter(ViewParamsFilter(field=Mapping.field, value=field))
            .filter(ViewParamsFilter(field=Mapping.field_name, value=field_name))
            .filter(ViewParamsFilter(field=Mapping.connection_name, value=app))
            .build()
        )
        mapping = await self.mapping_service.find_by_view_params_first(view_params)
        if mapping is None:
            mapping = Mapping(table=table, field=field, description='', field_name=field_name, connection_name=app)
            await self.mapping_service.save(mapping)

        sync_data = SyncData(
            service_model_info=json.dumps(service_model_info, sort_keys=True, default=str),
            template_context_type=json.dumps(template_context_type, sort_keys=True, default=str),
            template_context_default=json.dumps(template_context_default, sort_keys=True, default=str),
            history_context_default=json.dumps(history_context_default, sort_keys=True, default=str),
            parsed_model_type=json.dumps(parsed_model_type, sort_keys=True, default=str) if parsed_model_type else None,
            parsed_model_default=json.dumps(parsed_model_default, sort_keys=True,
                                            default=str) if parsed_model_default else None,
            fail_parse_model_strategy=fail_parse_model_strategy
        )

        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=MappingEntity.connection_name, value=app))
            .filter(ViewParamsFilter(field=MappingEntity.table, value=table))
            .filter(ViewParamsFilter(field=MappingEntity.field, value=field))
            .filter(ViewParamsFilter(field=MappingEntity.name, value=name))
            .filter(ViewParamsFilter(field=MappingEntity.entity, value='sync_data'))
            .build()
        )
        mapping_entities = await self.mapping_entity_service.find_by_view_params(view_params)
        need_save = True
        if len(mapping_entities) > 0:
            need_remove_sync_datas = []
            need_remove_mapping_entity = []
            for me in mapping_entities:
                sd = await self.sync_data_service.find_by_id(me.entity_id)
                if sd is None:
                    need_remove_mapping_entity.append(me)
                    continue
                if (
                        need_save and
                        sd.service_model_info == sync_data.service_model_info and
                        sd.template_context_type == sync_data.template_context_type and
                        sd.template_context_default == sync_data.template_context_default and
                        sd.history_context_default == sync_data.history_context_default and
                        sd.parsed_model_type == sync_data.parsed_model_type and
                        sd.parsed_model_default == sync_data.parsed_model_default and
                        sd.fail_parse_model_strategy == sync_data.fail_parse_model_strategy
                ):
                    need_save = False
                else:
                    need_remove_mapping_entity.append(me)
                    need_remove_sync_datas.append(sd)

            await self.mapping_entity_service.remove_all(need_remove_mapping_entity)
            await self.sync_data_service.remove_all(need_remove_sync_datas)

        if need_save:
            sync_data = await self.sync_data_service.save(sync_data)
            mapping_entity = MappingEntity(
                connection_name=app,
                table=table,
                field=field,
                name=name,
                entity='sync_data',
                entity_id=sync_data.id
            )
            await self.mapping_entity_service.save(mapping_entity)
