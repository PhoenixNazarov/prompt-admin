import asyncio

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.service.base import BasePermissionService
from promptadmin_server.api.service.preview_template_service import (
    PreviewTemplateService,
)
from promptadmin_server.api.service.prompt_load_service import PromptLoadService
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.data.entity.prompt_audit import PromptAudit
from promptadmin_server.data.service.mapping_service import MappingService
from settings import SETTINGS


class PermissionPromptService(BasePermissionService):
    def __init__(
        self,
        *args,
        preview_template_service: PreviewTemplateService | None = None,
        prompt_load_service: PromptLoadService | None = None,
        mapping_service: MappingService | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.preview_template_service = (
            preview_template_service or PreviewTemplateService()
        )
        self.prompt_load_service = prompt_load_service or PromptLoadService()
        self.mapping_service = mapping_service or MappingService()

    async def require_mapping_permission(
        self,
        mapping_id: int,
        value: int,
        user_data: UserData,
        key: str = "project_prompt",
    ):
        mapping = await self.mapping_service.find_by_id(mapping_id)
        if mapping is None:
            raise TypeCheckException()
        await self.require_project_permission(
            mapping.connection_name, key, value, user_data
        )
        return mapping

    async def load_all(self, user_data: UserData):
        # TODO: optimize
        mappings = await self.mapping_service.find_all()

        allow_projects = await self.connections_get_all(user_data)
        allow_mappings = [m for m in mappings if m.connection_name in allow_projects]

        res = await asyncio.gather(
            *[self.prompt_load_service.load_mapping(m) for m in allow_mappings]
        )
        out = []
        for i in res:
            out += i
        return out

    async def save(self, prompt: Prompt, user_data: UserData):
        mapping = await self.require_mapping_permission(prompt.mapping_id, 2, user_data)
        return await self.prompt_load_service.save(
            mapping.connection_name, prompt, user_data
        )

    async def preview(
        self,
        project: str,
        prompt: Prompt,
        context: dict | None,
        connection: str | None,
        user_data: UserData,
    ):
        await self.require_project_permission(project, "project_prompt", 1, user_data)
        return await self.preview_template_service.preview_prompt(
            prompt, context, connection
        )

    async def connections_get_all(self, user_data: UserData):
        allow_projects = await self.access_permission_service.get_allow_projects(
            user_data.account
        )
        return SETTINGS.connections.keys() & allow_projects

    async def get_prompt_audits(
        self, prompt: Prompt, count: int, page: int, user_data: UserData
    ) -> list[PromptAudit]:
        await self.require_mapping_permission(prompt.mapping_id, 1, user_data)
        return await self.prompt_load_service.get_prompt_audits(prompt, count, page)

    async def get_prompt_audits_count(self, prompt: Prompt, user_data: UserData) -> int:
        await self.require_mapping_permission(prompt.mapping_id, 1, user_data)
        return await self.prompt_load_service.get_prompt_audits_count(prompt)

    async def create_disable(
        self,
        connection_name: str,
        table: str,
        field: str,
        name: str,
        user_data: UserData,
    ):
        await self.require_project_permission(
            connection_name, "project_prompt", 2, user_data
        )
        return await self.prompt_load_service.create_disable(
            connection_name, table, field, name
        )

    async def get_disable(self, user_data: UserData):
        disables = await self.prompt_load_service.get_disable()
        allow_projects = await self.access_permission_service.get_allow_projects(
            user_data.account
        )
        return [r for r in disables if r.connection_name in allow_projects]
