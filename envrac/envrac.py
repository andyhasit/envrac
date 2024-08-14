import os
from datetime import date, datetime, time
from typing import Any
from collections.abc import Generator
from contextlib import contextmanager

from .config import Config
from .exceptions import EnvracChoiceError, EnvracRangeError, EnvracUnsetVariableError
from .parser import Parser
from .register import Register
from .utils import Undefined, is_null_string
from .types import ValueType


class _Env:
    """
    The class for `env` (a singleton).
    """

    def __init__(self):
        self._prefix = None
        self.config = Config()
        self._register = Register(self.config)
        self.parser = Parser(self.config)
        with self.prefix("ENVRAC_"):
            self.config.discovery_mode = self.bool("DISCOVERY_MODE", default=False)
            self.config.print_values = self.bool("PRINT_VALUES", default=False)

    def _getvar(
        self,
        name: str,
        type: ValueType,
        default: Any,
        read_none: bool = False,
        choices: list[Any] | None = None,
        min_val: Any = None,
        max_val: Any = None,
    ) -> Any:
        if self._prefix:
            name = f"{self._prefix}{name}"
        if isinstance(default, str):
            default = self.parser.parse(type, name, default)
        self._register.add(
            name=name,
            type=type,
            default=default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            read_none=read_none,
        )
        raw_value = os.environ.get(name)
        if raw_value is None:
            if default == Undefined:
                if not self.config.discovery_mode:
                    raise EnvracUnsetVariableError(name)
            else:
                final_value = default
        elif read_none and is_null_string(raw_value):
            return None
        else:
            final_value = self.parser.parse(type, name, raw_value)
        if any(
            [
                (min_val is not None and final_value < min_val),
                (max_val is not None and final_value > max_val),
            ]
        ):
            if not self.config.discovery_mode:
                raise EnvracRangeError(
                    name=name,
                    type=type,
                    value=final_value,
                    min_val=min_val,
                    max_val=max_val,
                    print_value=self.config.print_values,
                )
        if choices is not None and final_value not in choices:
            if not self.config.discovery_mode:
                raise EnvracChoiceError(
                    name=name,
                    type=type,
                    value=final_value,
                    choices=choices,
                    print_value=self.config.print_values,
                )
        return final_value

    @contextmanager
    def prefix(self, prefix: str) -> Generator:
        try:
            self._prefix = prefix
            yield
        finally:
            self._prefix = None

    def reset(self) -> None:
        self._register.reset()

    def put(self, name: str, value: Any = None) -> None:
        if value is None:
            del os.environ[name]
        else:
            os.environ[name] = str(value)

    def print(self, *order_by: str) -> None:
        self._register.print(*order_by)

    def dict(self, *fields, drop_prefix=False) -> dict:
        values = {}
        for field in fields:
            name, type, default, read_none = self.parser.parse_dict_field(field)
            val = self._getvar(name, type, default, read_none=read_none)
            if not drop_prefix and self._prefix:
                name = f"{self._prefix}{name}"
            values[name] = val
        return values

    def str(self, name, default=Undefined, choices=None, read_none=False) -> str | None:
        return self._getvar(
            name, ValueType.str, default, choices=choices, read_none=read_none
        )

    def bool(self, name, default=Undefined, read_none=False) -> bool | None:
        return self._getvar(name, ValueType.bool, default, read_none=read_none)

    def date(
        self,
        name,
        default=Undefined,
        choices=None,
        min_val=None,
        max_val=None,
        read_none=False,
    ) -> date | None:
        return self._getvar(
            name,
            ValueType.date,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            read_none=read_none,
        )

    def datetime(
        self,
        name,
        default=Undefined,
        choices=None,
        min_val=None,
        max_val=None,
        read_none=False,
    ) -> datetime | None:
        return self._getvar(
            name,
            ValueType.datetime,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            read_none=read_none,
        )

    def int(
        self,
        name,
        default=Undefined,
        choices=None,
        min_val=None,
        max_val=None,
        read_none=False,
    ) -> int | None:
        return self._getvar(
            name,
            ValueType.int,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            read_none=read_none,
        )

    def float(
        self,
        name,
        default=Undefined,
        choices=None,
        min_val=None,
        max_val=None,
        read_none=False,
    ) -> float | None:
        return self._getvar(
            name,
            ValueType.float,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            read_none=read_none,
        )

    def time(
        self,
        name,
        default=Undefined,
        choices=None,
        min_val=None,
        max_val=None,
        read_none=False,
    ) -> time | None:
        return self._getvar(
            name,
            ValueType.time,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            read_none=read_none,
        )


env = _Env()
