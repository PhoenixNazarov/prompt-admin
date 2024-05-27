from typing import Optional
import threading

from .block_entity import BlockEntity

from ..sql_sub_controller import SqlSubController
from ...dto.view_params import ViewParamsBuilder
from ...dto.view_params_filter import ViewParamsFilter

from .local_blocking import LocalBlocking

from sqlalchemy.exc import IntegrityError

from ...error.blocking_error import BlockingError


class BlockEntityRepository:
    def __init__(self, sql_controller: SqlSubController):
        self.sql_controller = sql_controller

    def try_block(self, name: str, id: int):
        thread_ident = threading.get_ident()
        LocalBlocking.check_register(thread_ident)
        info = LocalBlocking.get_info_about_thread(thread_ident)
        block = BlockEntity(entity_name=name, entity_ident=id, call_name=info['call_name'])
        try:
            block = self.sql_controller.save(block)
        except IntegrityError as exc:
            raise BlockingError('Already blocking') from exc
        LocalBlocking.create_block(thread_ident, block, self)

    def remove(self, entity: BlockEntity):
        self.sql_controller.remove(entity)

    def find_by_name_and_id(self, name: str, id: int) -> Optional[BlockEntity]:
        name_filter = ViewParamsFilter(field=BlockEntity.entity_name, value=name)
        ident_filter = ViewParamsFilter(field=BlockEntity.entity_ident, value=id)
        view_params = (ViewParamsBuilder()
                       .add_filter(name_filter)
                       .add_filter(ident_filter)
                       .build())
        return self.sql_controller.find_by_view_params_first(BlockEntity, view_params)

    def find_all(self) -> list[BlockEntity]:
        view_params = ViewParamsBuilder().build()
        return self.sql_controller.find_by_view_params_all(BlockEntity, view_params)
