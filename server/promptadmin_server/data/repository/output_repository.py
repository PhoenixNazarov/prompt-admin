from promptadmin_server.data.entity.output import Output
from promptadmin_server.commons.repository import AsyncBaseRepository


class OutputRepository(AsyncBaseRepository[Output]):
    def __init__(self):
        super().__init__(Output)
