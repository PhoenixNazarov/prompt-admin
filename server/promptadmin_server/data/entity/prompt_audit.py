from pydantic import BaseModel

from promptadmin_server.commons.entity.base_entity import BaseEntity


class PromptAuditData(BaseModel):
    mapping_id: int
    table: str
    field: str
    prompt_id: int | None
    value: str
    name: str | None

    account_id: int | None


class PromptAudit(BaseEntity, PromptAuditData, table=True):
    __tablename__ = 'pa_prompt_audit'
