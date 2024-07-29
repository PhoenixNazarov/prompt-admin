from typing import Any

from pydantic import BaseModel


class ViewParamsOrder(BaseModel):
    # Object for query "ORDER BY field [desc]" generation

    # BaseEntity field
    field: Any
    # Default ascending
    desc: bool = False
