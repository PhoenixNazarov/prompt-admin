from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin.api.service.format_service import FormatService

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
async def load(load_format_dto: LoadFormatDto):
    return format_service.load_calculate(load_format_dto.schema_json)


@router.post('/generate')
async def generate(generate_format_dto: GenerateFormatDto):
    return format_service.generate_calculate(generate_format_dto.input_object, generate_format_dto.mode)


@router.post('/validate')
async def validate(validation_input_dto: ValidationInputDto):
    return format_service.validate(validation_input_dto.schema_json, validation_input_dto.obj)
