import json
import logging
import subprocess
from tempfile import NamedTemporaryFile

from fastapi import APIRouter
from promptadmin.types import ModelServiceInfo, Message
from pydantic import BaseModel

from promptadmin_server.api.dto.prompt import Prompt
from promptadmin_server.api.routers.dependency import UserDependsAnnotated
from promptadmin_server.api.service.preview_template_service import PreviewTemplateService
from promptadmin_server.api.service.prompt_load_service import PromptLoadService

from settings import SETTINGS

logger = logging.getLogger(__name__)

router = APIRouter()

preview_template_service = PreviewTemplateService()
prompt_load_service = PromptLoadService()


class PreviewPromptDto(BaseModel):
    prompt: Prompt
    context: dict | None = None
    connection: str | None = None


class ExecutePromptDto(BaseModel):
    service_model_info: ModelServiceInfo
    history: list[Message]
    prompt: str
    parsed_model_type: dict | None = None


class ValidateJinjaDto(BaseModel):
    prompt: str


class ValidateResponseDto(BaseModel):
    j2lint: dict | None


@router.get('/load_all')
async def load_all():
    return await prompt_load_service.load_all()


@router.post('/save')
async def save(prompt: Prompt, user_data: UserDependsAnnotated):
    return await prompt_load_service.save(prompt, user_data)


@router.post('/preview')
async def preview(preview_prompt_dto: PreviewPromptDto):
    return await preview_template_service.preview_prompt(
        preview_prompt_dto.prompt,
        preview_prompt_dto.context,
        preview_prompt_dto.connection
    )


@router.post('/execute')
async def execute(execute_prompt_dto: ExecutePromptDto):
    return await preview_template_service.execute(
        execute_prompt_dto.service_model_info,
        execute_prompt_dto.prompt,
        execute_prompt_dto.history,
        execute_prompt_dto.parsed_model_type,
    )


@router.get('/connections/get_all')
async def connections_get_all():
    return list(SETTINGS.connections.keys())


@router.post('/validate')
async def validate(validate_jinja_dto: ValidateJinjaDto):
    tmp = NamedTemporaryFile(suffix='.j2')
    with open(tmp.name, 'w') as file:
        file.write(validate_jinja_dto.prompt)

    proc = subprocess.Popen(
        ['j2lint', file.name, '--json', '--ignore', 'S3', 'S6'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate(timeout=120)
    tmp.close()
    result_json = None
    try:
        result_json = json.loads(out)
    except Exception:
        pass
    return ValidateResponseDto(
        j2lint=result_json
    )
