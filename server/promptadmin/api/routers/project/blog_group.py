from fastapi import APIRouter

from promptadmin.api.routers.config.base_config_router_factory import bind_view
from promptadmin.data.entity.blog_group import BlogGroup
from promptadmin.data.service.blog_group_service import BlogGroupService

router = APIRouter()

service = BlogGroupService()

bind_view(router, BlogGroup, BlogGroup, service)
