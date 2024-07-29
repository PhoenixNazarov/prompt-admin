from promptadmin_server.commons.service.async_base_service import AsyncBaseService
from promptadmin_server.data.entity.variable import Variable
from promptadmin_server.data.repository.variable_repository import VariableRepository


class VariableService(AsyncBaseService[Variable]):
    def __init__(self, repository: VariableRepository = None):
        super().__init__(repository or VariableRepository())
