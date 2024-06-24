from typing import Any


def is_null_string(value: str) -> bool:
    return value.lower() in ("null", "none")


def print_table(rows: list[list[Any]]) -> None:
    """
    Prints rows in a table format.
    """

    def _row_str(row):
        return " ".join(str(col).ljust(size) for col, size in zip(row, sizes))

    zip(*rows)
    sizes = [max(map(lambda x: len(str(x)), col_values)) for col_values in zip(*rows)]
    header = _row_str(rows[0])
    print(header)
    print("-" * len(header))
    for row in rows[1:]:
        print(_row_str(row))


class _Undefined:
    """
    Class that represents undefined.
    """

    def __str__(self):
        return "<undefined>"

    def __eq__(self, other):
        return other.__class__ is _Undefined


Undefined = _Undefined()
