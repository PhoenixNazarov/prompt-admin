from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import (
    bind_service,
)
from promptadmin_server.api.service.permission.permission_blog_service import (
    permission_blog_post_service,
)
from promptadmin_server.data.entity.blog_post import BlogPost

router = APIRouter()


bind_service(permission_blog_post_service, BlogPost, router)
