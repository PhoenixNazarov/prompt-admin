from ...entity.base_entity import BaseEntity


class BlockEntity(BaseEntity, table=True):
    __tablename__ = 'block'

    entity_name: str
    entity_ident: int

    call_name: str = ''
    node: int = -1
    app: str = 'none'
