from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import (
    BasePermissionConfigService,
)
from promptadmin_server.data.entity.unit_test import UnitTest
from promptadmin_server.data.service.unit_test_service import UnitTestService

router = APIRouter()

config_service = BasePermissionConfigService(UnitTest, UnitTestService())
config_service.bind(router)
