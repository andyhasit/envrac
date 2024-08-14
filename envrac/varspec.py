from dataclasses import asdict, dataclass
from typing import Any

from .types import ValueType


@dataclass
class VarSpec:
    """
    Stores the specification of an environment variable, mainly for comparison purposes.
    """

    name: str
    type: ValueType
    default: Any
    choices: list[Any] | None = None
    read_none: bool = False
    min_val: Any = None
    max_val: Any = None

    def diff(self, other: "VarSpec") -> str | None:
        if self != other:
            diff_str = ""
            a, b = asdict(self), asdict(other)
            for k, v in a.items():
                if v != b[k]:
                    diff_str += f"\n    {k}: {v} != {b[k]}"
            return diff_str
        return None
