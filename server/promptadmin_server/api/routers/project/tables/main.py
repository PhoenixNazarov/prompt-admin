from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.data.entity.table_schema import TableSchema
from promptadmin_server.data.service.table_schema_service import TableSchemaService
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

table_schema_service = TableSchemaService()


class ProjectRequest(BaseModel):
    project: str


class UploadSchemaRequest(ProjectRequest):
    table_schema: dict


@router.post('/schema/download')
async def download(project_request: ProjectRequest):
    table_schema = await table_schema_service.find_by_key_first(TableSchema.project, project_request.project)

    json_compatible_item_data = jsonable_encoder(table_schema)
    return JSONResponse(content=json_compatible_item_data)


@router.post('/schema/upload')
async def upload(upload_schema_request: UploadSchemaRequest):
    table_schema = await table_schema_service.find_by_key_first(TableSchema.project, upload_schema_request.project)
    if table_schema:
        await table_schema_service.remove(table_schema)
    return await table_schema_service.save(
        TableSchema(
            project=upload_schema_request.project,
            table_schema=upload_schema_request.table_schema
        ))
