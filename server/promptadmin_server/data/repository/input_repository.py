from promptadmin_server.data.entity.input import Input
from promptadmin_server.commons.repository import AsyncBaseRepository


class InputRepository(AsyncBaseRepository[Input]):
    def __init__(self):
        super().__init__(Input)
