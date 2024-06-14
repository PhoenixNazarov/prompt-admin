from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin.api.service.format_service import FormatService
from promptadmin.api.service.user_data import UserData

format_service = FormatService()

router = APIRouter()


class LoadFormatDto(BaseModel):
    schema_json: str


class GenerateFormatDto(BaseModel):
    input_object: str
    mode: str


class ValidationInputDto(LoadFormatDto):
    obj: str


@router.post('/load')
async def load(request: Request, load_format_dto: LoadFormatDto):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()
    return format_service.load_calculate(load_format_dto.schema_json)


@router.post('/generate')
async def generate(request: Request, generate_format_dto: GenerateFormatDto):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()

    return format_service.generate_calculate(generate_format_dto.input_object, generate_format_dto.mode)


@router.post('/validate')
async def validate(request: Request, validation_input_dto: ValidationInputDto):
    user_data: UserData = request.scope['user_data']
    if user_data.account is None:
        raise ValueError()

    return format_service.validate(validation_input_dto.schema_json, validation_input_dto.obj)
