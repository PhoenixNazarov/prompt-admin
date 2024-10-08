from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.blog_post import BlogPost
from promptadmin_server.data.repository.blog_post_repository import BlogPostRepository


class BlogPostService(AsyncBaseService[BlogPost]):
    def __init__(self, repository: BlogPostRepository = None):
        super().__init__(repository or BlogPostRepository())
