import xmltodict
from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.data.entity.sync_data import SyncData
from promptadmin_server.data.service.sync_data_service import SyncDataService

router = APIRouter()

config_service = BasePermissionConfigService(SyncData, SyncDataService())
config_service.bind(router)


class ConvertXmlDto(BaseModel):
    obj: dict


@router.post("/convert/xml")
async def convert_xml(convert_xml_dto: ConvertXmlDto):
    return xmltodict.unparse(
        convert_xml_dto.obj,
        attr_prefix="attr_",
        full_document=False,
        pretty=True,
        indent=" " * 1,
    )
