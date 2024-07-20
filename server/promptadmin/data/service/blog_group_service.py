from promptadmin.commons.service.async_base_service import AsyncBaseService
from promptadmin.data.entity.blog_group import BlogGroup
from promptadmin.data.repository.blog_group_repository import BlogGroupRepository


class BlogGroupService(AsyncBaseService[BlogGroup]):
    def __init__(self, repository: BlogGroupRepository = None):
        super().__init__(repository or BlogGroupRepository())
