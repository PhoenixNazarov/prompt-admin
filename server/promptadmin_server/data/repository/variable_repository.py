from promptadmin_server.data.entity.variable import Variable
from promptadmin_server.commons.repository import AsyncBaseRepository


class VariableRepository(AsyncBaseRepository[Variable]):
    def __init__(self):
        super().__init__(Variable)
