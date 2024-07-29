from typing import Any

from pydantic import BaseModel
from enum import Enum


class ComparisonType(str, Enum):
    LT = 'LT'  # <
    LE = 'LE'  # <=
    EQ = 'EQ'  # ==
    NE = 'NE'  # !=
    GT = 'GT'  # >
    GE = 'GE'  # >=


class ViewParamsComparison(BaseModel):
    # Object for query "WHERE cmp value" generation

    # BaseEntity field
    field: Any
    # Value with a type of field
    value: Any
    # Sign to be used for comparison
    comparison: ComparisonType
