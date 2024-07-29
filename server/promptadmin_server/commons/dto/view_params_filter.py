from enum import Enum
from typing import Any

from pydantic import BaseModel


class ViewParamsFilter(BaseModel):
    # Object for query "WHERE field =/like value" generation

    # BaseEntity field
    field: Any
    # Value with a type of field
    value: Any
    # Use LIKE instead of =
    like: bool = False
