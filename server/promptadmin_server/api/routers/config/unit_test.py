from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.unit_test import UnitTest
from promptadmin_server.data.service.unit_test_service import UnitTestService

router = APIRouter()

unit_test_service = UnitTestService()

bind_view(router, UnitTest, UnitTest, unit_test_service)
