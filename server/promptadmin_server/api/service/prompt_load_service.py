from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.service.base import ConnectionMixin
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.commons.dto import (
    ViewParamsBuilder,
    ViewParamsFilter,
    ViewParamsOrder,
)
from promptadmin_server.data.entity.mapping import Mapping
from promptadmin_server.data.entity.mapping_entity import MappingEntity
from promptadmin_server.data.entity.prompt_audit import PromptAudit
from promptadmin_server.data.service.mapping_entity_service import MappingEntityService
from promptadmin_server.data.service.mapping_service import MappingService
from promptadmin_server.data.service.prompt_audit_service import PromptAuditService
from promptadmin_server.data.service.sync_data_service import SyncDataService
from promptadmin_server.data.service.unit_test_service import UnitTestService


class PromptLoadService(ConnectionMixin):
    def __init__(
        self,
        mapping_service: MappingService | None = None,
        prompt_audit_service: PromptAuditService | None = None,
        mapping_entity_service: MappingEntityService | None = None,
        sync_data_service: SyncDataService | None = None,
        unit_test_service: UnitTestService | None = None,
    ):
        self.mapping_service = mapping_service or MappingService()
        self.prompt_audit_service = prompt_audit_service or PromptAuditService()
        self.mapping_entity_service = mapping_entity_service or MappingEntityService()
        self.sync_data_service = sync_data_service or SyncDataService()
        self.unit_test_service = unit_test_service or UnitTestService()

    async def load_mapping(self, mapping: Mapping) -> list[Prompt]:
        if mapping.id is None:
            return []

        conn = await self.get_connection(mapping.connection_name)
        mapping_name = f", {mapping.field_name}" if mapping.field_name else ""
        order_name = f", {mapping.field_order}" if mapping.field_order else ""

        row = await conn.fetch(
            f"SELECT id, {mapping.field} {mapping_name} {order_name} FROM {mapping.table}"
        )

        result = []
        for i in row:
            result.append(
                Prompt(
                    mapping_id=mapping.id,
                    table=mapping.table,
                    field=mapping.field,
                    id=i["id"],
                    value=i[mapping.field],
                    name=i.get(mapping.field_name),
                    sort_value=i.get(mapping.field_order),
                )
            )
        return result

    async def load_mapping_name(self, mapping: Mapping, name: str) -> str:
        return await self.load(
            mapping.connection_name,
            mapping.field,
            mapping.table,
            mapping.field_name,
            name,
        )

    async def load(
        self, connection_name: str, field: str, table: str, field_name: str, name: str
    ) -> str:
        conn = await self.get_connection(connection_name)
        row = await conn.fetchrow(
            f"SELECT {field} FROM {table} WHERE {field_name} = $1", name
        )
        return row.get(field, "")

    async def save(self, project: str, prompt: Prompt, user_data: UserData):
        if user_data.account is None or user_data.account.id is None:
            raise TypeCheckException()
        conn = await self.get_connection(project)
        await self.prompt_audit_service.save(
            PromptAudit(
                mapping_id=prompt.mapping_id,
                table=prompt.table,
                field=prompt.field,
                value=prompt.value,
                account_id=user_data.account.id,
                prompt_id=prompt.id,
                name=prompt.name,
            )
        )
        sql = f"UPDATE {prompt.table} SET {prompt.field} = $1 WHERE id = $2"
        await conn.execute(sql, prompt.value, prompt.id)

        view_params = (
            ViewParamsBuilder()
            .filter(
                ViewParamsFilter(field=MappingEntity.connection_name, value=project)
            )
            .filter(ViewParamsFilter(field=MappingEntity.table, value=prompt.table))
            .filter(ViewParamsFilter(field=MappingEntity.field, value=prompt.field))
            .filter(ViewParamsFilter(field=MappingEntity.entity, value="sync_data"))
            .build()
        )
        mapping_entities = await self.mapping_entity_service.find_by_view_params(
            view_params
        )
        if len(mapping_entities) <= 0:
            return
        sync_data = await self.sync_data_service.find_by_id(
            mapping_entities[0].entity_id
        )
        if sync_data is None or sync_data.id is None or prompt.name is None:
            return
        unit_test = await self.unit_test_service.find_by_sync_data_name(
            sync_data.id, prompt.name
        )
        if unit_test is None:
            return
        unit_test.test_status = "wait"
        unit_test.test_preview = None
        unit_test.test_response_model = None
        unit_test.test_exception = None
        await self.unit_test_service.save(unit_test)

    @staticmethod
    def _build_prompt_audit(prompt: Prompt):
        return (
            ViewParamsBuilder()
            .filter(
                ViewParamsFilter(field=PromptAudit.mapping_id, value=prompt.mapping_id)
            )
            .filter(ViewParamsFilter(field=PromptAudit.table, value=prompt.table))
            .filter(ViewParamsFilter(field=PromptAudit.field, value=prompt.field))
            .filter(ViewParamsFilter(field=PromptAudit.prompt_id, value=prompt.id))
            .filter(ViewParamsFilter(field=PromptAudit.name, value=prompt.name))
            .order(ViewParamsOrder(field=PromptAudit.id, desc=True))
        )

    async def get_prompt_audits(
        self, prompt: Prompt, count: int, page: int
    ) -> list[PromptAudit]:
        view_params = self._build_prompt_audit(prompt).count(count).page(page).build()
        return await self.prompt_audit_service.find_by_view_params(view_params)

    async def get_prompt_audits_count(self, prompt: Prompt) -> int:
        view_params = self._build_prompt_audit(prompt).build()
        return await self.prompt_audit_service.count_by_view_params(view_params)

    async def create_disable(
        self, connection_name: str, table: str, field: str, name: str
    ):
        mapping_entity = MappingEntity(
            connection_name=connection_name,
            table=table,
            field=field,
            name=name,
            entity="disable",
            entity_id=1,
        )
        return await self.mapping_entity_service.save(mapping_entity)

    async def get_disable(self):
        return await self.mapping_entity_service.find_by_key(
            MappingEntity.entity, "disable"
        )
