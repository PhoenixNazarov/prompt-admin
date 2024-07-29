from ..entity.blog_post import BlogPost
from ...commons.repository import AsyncBaseRepository


class BlogPostRepository(AsyncBaseRepository[BlogPost]):
    def __init__(self):
        super().__init__(BlogPost)
