from promptadmin_server.commons.entity.base_entity import BaseEntity


class HealthTarget(BaseEntity, table=True):
    __tablename__ = "pa_health_target"

    url: str
    title: str
