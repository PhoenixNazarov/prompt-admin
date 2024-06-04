import asyncio

import asyncpg
from fastapi import APIRouter, Request

from promptadmin.api.dto.prompt import Prompt
from promptadmin.api.service.preview_template_service import PreviewTemplateService
from promptadmin.api.service.user_data import UserData
from promptadmin.data.entity.mapping import Mapping
from promptadmin.data.entity.prompt_audit import PromptAudit
from promptadmin.data.service.mapping_service import MappingService
from promptadmin.data.service.prompt_audit_service import PromptAuditService

from settings import SETTINGS

router = APIRouter()

mapping_service = MappingService()
preview_template_service = PreviewTemplateService()
prompt_audit_service = PromptAuditService()


@router.get('/load_all')
async def load_all(request: Request):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()

    async def load_mapping(mapping: Mapping) -> list[Prompt]:
        conn = await asyncpg.connect(SETTINGS.connections[mapping.connection_name])
        mapping_name = f', {mapping.field_name}' if mapping.field_name else ''

        row = await conn.fetch(f'SELECT id, {mapping.field} {mapping_name} FROM {mapping.table}')

        result = []
        for i in row:
            result.append(
                Prompt(
                    mapping_id=mapping.id,
                    table=mapping.table,
                    field=mapping.field,
                    id=i['id'],
                    value=i[mapping.field],
                    name=i.get(mapping.field_name)
                )
            )
        return result

    mappings = await mapping_service.find_all()

    res = await asyncio.gather(*[load_mapping(m) for m in mappings])

    out = []
    for i in res:
        out += i

    return out


@router.post('/save')
async def save(prompt: Prompt, request: Request):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    mapping = await mapping_service.find_by_table_field(prompt.table, prompt.field)
    conn = await asyncpg.connect(SETTINGS.connections[mapping.connection_name])
    await prompt_audit_service.save(
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


@router.post('/preview')
async def preview(prompt: Prompt, request: Request):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    return await preview_template_service.preview_prompt(prompt)
