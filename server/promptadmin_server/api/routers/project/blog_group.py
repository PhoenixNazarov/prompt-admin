from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.blog_group import BlogGroup
from promptadmin_server.data.service.blog_group_service import BlogGroupService

router = APIRouter()

service = BlogGroupService()

bind_view(router, BlogGroup, BlogGroup, service)
