import asyncio
import logging

import asyncpg

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.commons.dto import ViewParamsBuilder, ViewParamsFilter
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.entity.prompt_audit import PromptAudit
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService
from promptadmin_server.data.service.prompt_audit_service import PromptAuditService
from promptadmin_server.data.service.sync_data_service import SyncDataService
from promptadmin_server.data.service.unit_test_service import UnitTestService
from settings import SETTINGS

logger = logging.getLogger(__name__)


class PromptLoadService:
    def __init__(self,
                 mapping_service: MappingService = None,
                 prompt_audit_service: PromptAuditService = None,
                 mapping_entity_service: MappingEntityService = None,
                 sync_data_service: SyncDataService = None,
                 unit_test_service: UnitTestService = None
                 ):
        self.mapping_service = mapping_service or MappingService()
        self.prompt_audit_service = prompt_audit_service or PromptAuditService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()
        self.sync_data_service = sync_data_service or SyncDataService()
        self.unit_test_service = unit_test_service or UnitTestService()

    @staticmethod
    async def load_mapping(mapping: Mapping) -> list[Prompt]:
        try:
            conn = await asyncpg.connect(SETTINGS.connections[mapping.connection_name])
        except Exception as e:
            logger.error('Error connection database', exc_info=e)
            return []

        mapping_name = f', {mapping.field_name}' if mapping.field_name else ''
        order_name = f', {mapping.field_order}' if mapping.field_order else ''

        row = await conn.fetch(f'SELECT id, {mapping.field} {mapping_name} {order_name} FROM {mapping.table}')

        result = []
        for i in row:
            result.append(
                Prompt(
                    mapping_id=mapping.id,
                    table=mapping.table,
                    field=mapping.field,
                    id=i['id'],
                    value=i[mapping.field],
                    name=i.get(mapping.field_name),
                    sort_value=i.get(mapping.field_order)
                )
            )
        return result

    async def load_all(self):
        mappings = await self.mapping_service.find_all()
        res = await asyncio.gather(*[self.load_mapping(m) for m in mappings])
        out = []
        for i in res:
            out += i
        return out

    async def load_mapping_name(self, mapping: Mapping, name: str) -> str:
        return await self.load(
            mapping.connection_name,
            mapping.field,
            mapping.table,
            mapping.field_name,
            name,
        )

    @staticmethod
    async def load(connection_name: str, field: str, table: str, field_name: str, name: str) -> str:
        try:
            conn = await asyncpg.connect(SETTINGS.connections[connection_name])
        except Exception as e:
            logger.error('Error connection database', exc_info=e)
            return ''

        name = f'WHERE {field_name} = \'{name}\''

        row = await conn.fetch(f'SELECT {field} FROM {table} {name}')
        return row[0].get(field, '')

    async def save(self, prompt: Prompt, user_data: UserData):
        mapping = await self.mapping_service.find_by_id(prompt.mapping_id)
        conn = await asyncpg.connect(SETTINGS.connections[mapping.connection_name])
        await self.prompt_audit_service.save(
            PromptAudit(
                mapping_id=prompt.mapping_id,
                table=prompt.table,
                field=prompt.field,
                value=prompt.value,
                account_id=user_data.account.id,
                prompt_id=prompt.id,
                name=prompt.name
            )
        )
        sql = f"UPDATE {prompt.table} SET {prompt.field} = $1 WHERE id = $2"
        await conn.execute(sql, prompt.value, prompt.id)

        view_params = (
            ViewParamsBuilder()
            .filter(ViewParamsFilter(field=MappingEntity.connection_name, value=mapping.connection_name))
            .filter(ViewParamsFilter(field=MappingEntity.table, value=prompt.table))
            .filter(ViewParamsFilter(field=MappingEntity.field, value=prompt.field))
            .filter(ViewParamsFilter(field=MappingEntity.entity, value='sync_data'))
            .build()
        )
        mapping_entities = await self.mapping_entity_service.find_by_view_params(view_params)
        if len(mapping_entities) <= 0:
            return
        sync_data = await self.sync_data_service.find_by_id(mapping_entities[0].entity_id)
        if sync_data is None:
            return
        unit_test = await self.unit_test_service.find_by_sync_data_name(sync_data.id, prompt.name)
        if unit_test is None:
            return
        unit_test.test_status = 'wait'
        await self.unit_test_service.save(unit_test)
