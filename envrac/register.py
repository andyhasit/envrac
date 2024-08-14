import os
from operator import attrgetter

from .config import Config
from .exceptions import EnvracSpecificationError
from .utils import print_table
from .varspec import VarSpec


class Register:
    def __init__(self, config=Config):
        self.vars = {}
        self.config = config

    def add(self, **kwargs) -> None:
        spec = VarSpec(**kwargs)
        if match := self.vars.get(spec.name, None):
            if diff := match.diff(spec):
                raise EnvracSpecificationError(name=spec.name, diff=diff)
        else:
            self.vars[spec.name] = spec

    def reset(self) -> None:
        self.vars.clear()

    def list(self, *order_by: str) -> list[VarSpec]:
        if not order_by:
            order_by = ("name",)
        return sorted(self.vars.values(), key=attrgetter(*order_by))

    def print(self, *order_by: str) -> None:
        header = [
            "NAME",
            "TYPE",
            "DEFAULT",
            "READ_NONE",
            "CHOICES",
            "MIN",
            "MAX",
        ]
        if self.config.print_values:
            header.append("RAW")
        rows = [header]
        for spec in self.list(*order_by):
            row = [
                spec.name,
                spec.type.value,
                spec.default,
                spec.read_none,
                len(spec.choices) if spec.choices else None,
                spec.min_val,
                spec.max_val,
            ]
            if self.config.print_values:
                row.append(os.getenv(spec.name))
            rows.append(row)
        print_table(rows)
