import xmltodict
from fastapi import APIRouter
from pydantic import BaseModel

from promptadmin.api.routers.config.base_config_router_factory import bind_view
from promptadmin.data.entity.sync_data import SyncData
from promptadmin.data.service.sync_data_service import SyncDataService

router = APIRouter()

sync_data_service = SyncDataService()

bind_view(router, SyncData, SyncData, sync_data_service)


class ConvertXmlDto(BaseModel):
    obj: dict


@router.post('/convert/xml')
async def convert_xml(convert_xml_dto: ConvertXmlDto):
    return xmltodict.unparse(convert_xml_dto.obj, attr_prefix='attr_', full_document=False, pretty=True, indent=' ' * 1)
