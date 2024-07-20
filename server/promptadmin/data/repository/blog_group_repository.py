from ..entity.blog_group import BlogGroup
from ...commons.repository import AsyncBaseRepository


class BlogGroupRepository(AsyncBaseRepository[BlogGroup]):
    def __init__(self):
        super().__init__(BlogGroup)
