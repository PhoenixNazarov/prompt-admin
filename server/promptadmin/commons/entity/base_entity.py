import datetime
from typing import Any, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


def __eq__(self, other: Any) -> bool:
    if isinstance(other, BaseModel):
        # When comparing instances of generic types for equality, as long as all field values are equal,
        # only require their generic origin types to be equal, rather than exact type equality.
        # This prevents headaches like MyGeneric(x=1) != MyGeneric[Any](x=1).
        self_type = self.__pydantic_generic_metadata__['origin'] or self.__class__
        other_type = other.__pydantic_generic_metadata__['origin'] or other.__class__

        dict1 = self.__dict__.copy()
        dict2 = other.__dict__.copy()

        if '_sa_instance_state' in dict1:
            dict1.pop('_sa_instance_state')
        if '_sa_instance_state' in dict2:
            dict2.pop('_sa_instance_state')

        return (
                self_type == other_type
                and dict1 == dict2
        )
        # and self.__pydantic_private__ == other.__pydantic_private__
        # and self.__pydantic_extra__ == other.__pydantic_extra__
    else:
        return NotImplemented  # delegate to the other item in the comparison


SQLModel.__eq__ = __eq__


class BaseEntity(SQLModel):
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    time_create: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now())
