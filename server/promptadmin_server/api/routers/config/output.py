from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.output import Output, OutputData
from promptadmin_server.data.service.output_service import OutputService

router = APIRouter()

output_service = OutputService()

bind_view(router, OutputData, Output, output_service)
