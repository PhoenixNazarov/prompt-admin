from promptadmin_server.api.exceptions import TypeCheckException
from promptadmin_server.api.service.base import (
    AbstractConfigService,
    BasePermissionService,
)
from promptadmin_server.api.service.user_data import UserData
from promptadmin_server.commons.entity import BaseEntity
from promptadmin_server.commons.service import AsyncBaseService
from promptadmin_server.data.entity.blog_group import BlogGroup
from promptadmin_server.data.entity.blog_post import BlogPost
from promptadmin_server.data.service.blog_group_service import BlogGroupService
from promptadmin_server.data.service.blog_post_service import BlogPostService


__all__ = ["permission_blog_group_service", "permission_blog_post_service"]


class PermissionBlogService(AbstractConfigService, BasePermissionService):
    def __init__(
        self, *args, entity: type[BaseEntity], service: AsyncBaseService, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.entity = entity
        self.service = service

    async def get_all(self, user_data: UserData):
        raise TypeCheckException()

    async def save(self, _entity: BlogGroup, user_data: UserData):
        await self.require_project_permission(
            _entity.project, "project_blog", 2, user_data
        )
        return await self.service.save(_entity)

    async def remove(self, id_: int, user_data: UserData):
        entity = await self.service.find_by_id(id_)
        if entity is None:
            raise TypeCheckException()
        await self.require_project_permission(
            entity.project, "project_blog", 2, user_data
        )
        return await self.service.remove(entity)

    async def find_by_key(self, key: str, val: str | int | bool, user_data: UserData):
        if key != "project" or not isinstance(val, str):
            raise TypeCheckException()
        await self.require_project_permission(val, "project_blog", 1, user_data)
        return await self.service.find_by_key(getattr(self.entity, key, None), val)


permission_blog_group_service = PermissionBlogService(
    entity=BlogGroup, service=BlogGroupService()
)
permission_blog_post_service = PermissionBlogService(
    entity=BlogPost, service=BlogPostService()
)
