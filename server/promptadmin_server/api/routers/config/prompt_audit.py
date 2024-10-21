from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.permission.permission_prompt_service import (
    PermissionPromptService,
)

router = APIRouter()

permission_prompt_service = PermissionPromptService()


class GetTablePrompt(BaseModel):
    prompt: Prompt
    item_per_page: int
    page: int


@router.post("/get")
async def get(get_table_prompt: GetTablePrompt, user_data: UserDependsAnnotated):
    return await permission_prompt_service.get_prompt_audits(
        get_table_prompt.prompt,
        get_table_prompt.item_per_page,
        get_table_prompt.page,
        user_data,
    )


@router.post("/get/count")
async def get_count(get_table_prompt: GetTablePrompt, user_data: UserDependsAnnotated):
    return await permission_prompt_service.get_prompt_audits_count(
        get_table_prompt.prompt,
        user_data,
    )
