from fastapi import APIRouter, Request

from promptadmin.api.dto.prompt import Prompt
from promptadmin.api.service.user_data import UserData
from promptadmin.commons.dto import ViewParamsBuilder, ViewParamsFilter, ViewParamsOrder
from promptadmin.data.entity.prompt_audit import PromptAudit
from promptadmin.data.service.prompt_audit_service import PromptAuditService

router = APIRouter()

prompt_audit_service = PromptAuditService()


@router.post('/get')
async def get(request: Request, prompt: Prompt):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    view_params = (
        ViewParamsBuilder()
        .filter(ViewParamsFilter(field=PromptAudit.mapping_id, value=prompt.mapping_id))
        .filter(ViewParamsFilter(field=PromptAudit.table, value=prompt.table))
        .filter(ViewParamsFilter(field=PromptAudit.field, value=prompt.field))
        .filter(ViewParamsFilter(field=PromptAudit.prompt_id, value=prompt.id))
        .filter(ViewParamsFilter(field=PromptAudit.name, value=prompt.name))
        .count(10)
        .order(ViewParamsOrder(field=PromptAudit.time_create, desc=True))
        .build()
    )

    return await prompt_audit_service.find_by_view_params(view_params)
