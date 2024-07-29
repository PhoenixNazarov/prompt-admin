from promptadmin_server.commons.entity.base_entity import BaseEntity


class BlogPost(BaseEntity, table=True):
    __tablename__ = 'pa_blog_post'

    project: str
    title: str
    content: str
    group_id: int | None
