from promptadmin_server.commons.entity.base_entity import BaseEntity


class BlogGroup(BaseEntity, table=True):
    __tablename__ = 'pa_blog_group'

    project: str
    title: str
