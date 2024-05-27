from promptadmin.data.entity.output import Output
from promptadmin.commons.repository import AsyncBaseRepository


class OutputRepository(AsyncBaseRepository[Output]):
    def __init__(self):
        super().__init__(Output)
