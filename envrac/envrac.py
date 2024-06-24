from typing import Any
import os
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
        nullable: bool = False,
        choices: list[Any] | None = None,
        min_val: Any = None,
        max_val: Any = None,
    ) -> Any:
        if self._prefix:
            name = f"{self._prefix}{name}"
        self._register.add(
            name=name,
            type=type,
            default=default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            nullable=nullable,
        )
        raw_value = os.environ.get(name)
        if raw_value is None:
            if default == Undefined:
                if not self.config.discovery_mode:
                    raise EnvracUnsetVariableError(name)
            else:
                final_value = default
        elif nullable and is_null_string(raw_value):
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
    def prefix(self, prefix: str):
        try:
            self._prefix = prefix
            yield
        finally:
            self._prefix = None

    def clear(self):
        self._register.clear()

    def print(self, *order_by: str):
        self._register.print(*order_by)

    def dict(self, *fields, drop_prefix=False) -> dict:
        values = {}
        for field in fields:
            name, type, default, nullable = self.parser.parse_dict_field(field)
            val = self._getvar(name, type, default, nullable=nullable)
            if not drop_prefix and self._prefix:
                name = f"{self._prefix}{name}"
            values[name] = val
        return values

    def str(self, name, default=Undefined, choices=None):
        return self._getvar(name, ValueType.str, default, choices=choices)

    def str_(self, name, default=Undefined, choices=None):
        return self._getvar(
            name, ValueType.str, default, choices=choices, nullable=True
        )

    def bool(self, name, default=Undefined):
        return self._getvar(name, ValueType.bool, default)

    def bool_(self, name, default=Undefined):
        return self._getvar(name, ValueType.bool, default, nullable=True)

    def date(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.date,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
        )

    def date_(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.date,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            nullable=True,
        )

    def datetime(
        self, name, default=Undefined, choices=None, min_val=None, max_val=None
    ):
        return self._getvar(
            name,
            ValueType.datetime,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
        )

    def datetime_(
        self, name, default=Undefined, choices=None, min_val=None, max_val=None
    ):
        return self._getvar(
            name,
            ValueType.datetime,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            nullable=True,
        )

    def int(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.int,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
        )

    def int_(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.int,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            nullable=True,
        )

    def float(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.float,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
        )

    def float_(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.float,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            nullable=True,
        )

    def time(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.time,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
        )

    def time_(self, name, default=Undefined, choices=None, min_val=None, max_val=None):
        return self._getvar(
            name,
            ValueType.time,
            default,
            choices=choices,
            min_val=min_val,
            max_val=max_val,
            nullable=True,
        )


env = _Env()
