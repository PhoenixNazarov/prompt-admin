from promptadmin_server.data.entity.macro import Macro
from promptadmin_server.commons.repository import AsyncBaseRepository


class MacroRepository(AsyncBaseRepository[Macro]):
    def __init__(self):
        super().__init__(Macro)
