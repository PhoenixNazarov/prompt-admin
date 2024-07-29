from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.prompt_audit import PromptAudit
from promptadmin_server.data.repository.prompt_audit_repository import PromptAuditRepository


class PromptAuditService(AsyncBaseService[PromptAudit]):
    def __init__(self, repository: PromptAuditRepository = None):
        super().__init__(repository or PromptAuditRepository())
