from .sql_sub_controller import SqlSubController
from .async_sql_sub_controller import AsyncSqlSubController
from .block.block_entity_repository import BlockEntityRepository
from ..error.init_error import InitError
from ..singleton_metaclass import Singleton

from settings import SETTINGS


class SqlController(metaclass=Singleton):
    def __init__(self):
        self.sub_controllers: dict[str, SqlSubController] = {}
        self.block_repositories: dict[str, BlockEntityRepository] = {}
        self.async_sub_controllers: dict[str, AsyncSqlSubController] = {}

        for i in SETTINGS.database:
            dialect_drive = i.dialect
            if i.driver:
                dialect_drive += f'+{i.driver}'
            dsn = f'{dialect_drive}://{i.username}:{i.password}@{i.host}:{i.port}/{i.database}'
            if i.async_:
                async_sql_sub_controller = AsyncSqlSubController(dsn)
                self.async_sub_controllers[i.database_prefix] = async_sql_sub_controller
            else:
                sql_sub_controller = SqlSubController(dsn)
                self.sub_controllers[i.database_prefix] = sql_sub_controller
                self.block_repositories[i.database_prefix] = BlockEntityRepository(sql_sub_controller)

        self.supported_sub_controllers = self.sub_controllers.keys()
        self.async_supported_sub_controllers = self.async_sub_controllers.keys()

    def get_by_module(self, module: str) -> SqlSubController:
        module = module.lower()
        if module in self.supported_sub_controllers:
            return self.sub_controllers[module]
        if '' in self.supported_sub_controllers:
            return self.sub_controllers['']
        raise InitError('Module not support and default not set')

    def get_async_by_module(self, module: str) -> AsyncSqlSubController:
        module = module.lower()
        if module in self.async_supported_sub_controllers:
            return self.async_sub_controllers[module]
        if '' in self.async_supported_sub_controllers:
            return self.async_sub_controllers['']
        raise InitError('Module not support and default not set')

    def get_block_by_module(self, module: str) -> BlockEntityRepository:
        module = module.lower()
        if module in self.supported_sub_controllers:
            return self.block_repositories[module]
        if '' in self.supported_sub_controllers:
            return self.block_repositories['']
        raise InitError('Module not support and default not set')
