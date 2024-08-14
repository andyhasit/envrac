from datetime import date, datetime, time
from typing import Any
from collections.abc import Callable

from .config import Config
from .utils import Undefined
from .exceptions import EnvracParsingError, EnvracDictFieldError
from .types import ValueType

BOOLEAN_VALUES = ("1", "0", "true", "false")
BOOLEAN_TRUE = ("1", "true")


def parse_bool(value: str) -> bool:
    value = value.lower()
    if value not in BOOLEAN_VALUES:
        raise ValueError("Cannot parse to Boolean")
    return value in BOOLEAN_TRUE


class Parser:

    def __init__(self, config: Config):
        self.config = config
        self.converters: dict[ValueType, Callable] = {
            ValueType.int: int,
            ValueType.float: float,
            ValueType.bool: parse_bool,
            ValueType.str: str,
            ValueType.date: date.fromisoformat,
            ValueType.datetime: datetime.fromisoformat,
            ValueType.time: time.fromisoformat,
        }
        self.format_strs: dict[ValueType, str] = {
            ValueType.bool: "1/0/true/false (case insensitive)",
            ValueType.date: "YYYY-MM-DD",
            ValueType.datetime: "YYYY-MM-DD HH:MM:SS",
            ValueType.time: "HH:MM:SS",
        }

    def parse(self, type: ValueType, name: str, value: str) -> Any:
        try:
            return self.converters[type](value)
        except ValueError:
            pass
        # Need to do this outside the except block else it prints the ValueError, which
        # may contain sensitive information.
        raise EnvracParsingError(
            name=name,
            type=type,
            value=value,
            format_str=self.format_strs.get(type),
            print_value=self.config.print_values,
        )

    def parse_dict_field(self, field: str) -> tuple[str, ValueType, Any, bool]:
        """
        Example fields:
            FOO          # read FOO as a string
            FOO=bar      # read FOO as a string, default to 'bar'
            FOO:int      # read FOO as an int
            FOO:int=0    # read FOO as an int, default to 0
            ?FOO:int     # read FOO as an int, but allow 'NULL'
            ?FOO:int=0   # read FOO as an int, default to 0, but allow 'NULL'
        """
        # special char order check
        read_none = False
        default_str = None
        type_str = "str"
        if field.startswith("?"):
            read_none = True
            field = field[1:]
        if ":" in field:
            name, field = field.split(":")
            if "=" in field:
                type_str, default_str = field.split("=")
            else:
                type_str = field
        elif "=" in field:
            name, default_str = field.split("=")
        else:
            name = field

        try:
            type = ValueType(type_str)
        except ValueError:
            raise EnvracDictFieldError(
                f"Type {type} specified in `env.dict` is not valid."
            )

        if default_str is not None:
            default = self.parse(type, name, default_str)
        else:
            default = Undefined

        return name, type, default, read_none
