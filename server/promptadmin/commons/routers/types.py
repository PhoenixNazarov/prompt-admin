from datetime import datetime
from typing import TypeAlias, Union, Sequence, Dict

from pydantic import BaseModel

JsonDecodable = Union[
    float,
    int,
    bool,
    str,
    bytes,
]

SendableMessage: TypeAlias = Union[
    Dict[str, Union[JsonDecodable, datetime]],
    Sequence[Union[JsonDecodable, datetime]],
    Union[JsonDecodable, datetime],
    datetime,
    BaseModel,
    None,
]
