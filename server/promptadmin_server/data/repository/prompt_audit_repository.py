from promptadmin_server.data.entity.prompt_audit import PromptAudit
from promptadmin_server.commons.repository import AsyncBaseRepository


class PromptAuditRepository(AsyncBaseRepository[PromptAudit]):
    def __init__(self):
        super().__init__(PromptAudit)
