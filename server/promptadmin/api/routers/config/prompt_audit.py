from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin.api.dto.prompt import Prompt
from promptadmin.api.service.user_data import UserData
from promptadmin.commons.dto import ViewParamsBuilder, ViewParamsFilter, ViewParamsOrder
from promptadmin.data.entity.prompt_audit import PromptAudit
from promptadmin.data.service.prompt_audit_service import PromptAuditService

router = APIRouter()

prompt_audit_service = PromptAuditService()


class GetTablePrompt(BaseModel):
    prompt: Prompt
    item_per_page: int
    page: int


@router.post('/get')
async def get(request: Request, get_table_prompt: GetTablePrompt):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    prompt = get_table_prompt.prompt
    view_params = (
        ViewParamsBuilder()
        .filter(ViewParamsFilter(field=PromptAudit.mapping_id, value=prompt.mapping_id))
        .filter(ViewParamsFilter(field=PromptAudit.table, value=prompt.table))
        .filter(ViewParamsFilter(field=PromptAudit.field, value=prompt.field))
        .filter(ViewParamsFilter(field=PromptAudit.prompt_id, value=prompt.id))
        .filter(ViewParamsFilter(field=PromptAudit.name, value=prompt.name))
        .count(get_table_prompt.item_per_page)
        .page(get_table_prompt.page)
        .order(ViewParamsOrder(field=PromptAudit.time_create, desc=True))
        .build()
    )

    return await prompt_audit_service.find_by_view_params(view_params)


@router.post('/get/count')
async def get_count(request: Request, get_table_prompt: GetTablePrompt):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    prompt = get_table_prompt.prompt
    view_params = (
        ViewParamsBuilder()
        .filter(ViewParamsFilter(field=PromptAudit.mapping_id, value=prompt.mapping_id))
        .filter(ViewParamsFilter(field=PromptAudit.table, value=prompt.table))
        .filter(ViewParamsFilter(field=PromptAudit.field, value=prompt.field))
        .filter(ViewParamsFilter(field=PromptAudit.prompt_id, value=prompt.id))
        .filter(ViewParamsFilter(field=PromptAudit.name, value=prompt.name))
        .count(get_table_prompt.item_per_page)
        .page(get_table_prompt.page)
        .order(ViewParamsOrder(field=PromptAudit.time_create, desc=True))
        .build()
    )

    return await prompt_audit_service.count_by_view_params(view_params)
