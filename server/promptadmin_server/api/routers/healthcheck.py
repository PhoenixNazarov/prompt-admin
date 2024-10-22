from fastapi import APIRouter, Request
from pydantic import BaseModel

from promptadmin_server.api.service.permission.permission_healthcheck_service import (
    PermissionHealthCheckService,
)
from promptadmin_server.api.service.user_data import UserData

permission_healthcheck_service = PermissionHealthCheckService()

router = APIRouter()


class TargetIdsRequest(BaseModel):
    targets_ids: list[int]


class TargetRequest(BaseModel):
    url: str
    label: str


@router.get("/targets/load")
async def targets_load(request: Request):
    user_data: UserData = request.scope["user_data"]
    return await permission_healthcheck_service.load_all_target(user_data)


@router.post("/days/load")
async def days_load(request: Request, target_request: TargetIdsRequest):
    user_data: UserData = request.scope["user_data"]
    return await permission_healthcheck_service.load_last_days(
        target_request.targets_ids, user_data
    )


@router.post("/units/load")
async def units_load(request: Request, target_request: TargetIdsRequest):
    user_data: UserData = request.scope["user_data"]
    return await permission_healthcheck_service.load_units(
        target_request.targets_ids, user_data
    )


@router.post("/target/create")
async def target_create(request: Request, target_request: TargetRequest):
    user_data: UserData = request.scope["user_data"]
    return await permission_healthcheck_service.create_target(
        target_request.url, target_request.label, user_data
    )
