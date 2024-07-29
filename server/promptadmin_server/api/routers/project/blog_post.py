from fastapi import APIRouter

from promptadmin_server.api.routers.config.base_config_router_factory import bind_view
from promptadmin_server.data.entity.blog_post import BlogPost
from promptadmin_server.data.service.blog_post_service import BlogPostService

router = APIRouter()

service = BlogPostService()

bind_view(router, BlogPost, BlogPost, service)
