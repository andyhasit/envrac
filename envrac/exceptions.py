from typing import Any

from .types import ValueType

HIDDEN_VALUE = "***HIDDEN***"


class EnvracException(BaseException):
    def __init__(self, *msg: str):
        self.msgs = msg

    def __str__(self):
        msg = "\n  ".join(self.msgs)
        return f"\n  {msg}\n  See envrac documentation for help."


class EnvracChoiceError(EnvracException):
    def __init__(
        self,
        name: str,
        type: ValueType,
        value: str,
        choices: list[Any],
        print_value: bool = False,
    ):
        if not print_value:
            value = HIDDEN_VALUE
        choices_str = ", ".join(map(lambda s: f'"{s}"', choices))
        if len(choices_str) > 100:
            choices_str = choices_str[:100] + "..."
        msgs = [
            f'Environment variable "{name}" must be one of {choices_str}.',
            f"value: {value}",
        ]
        super().__init__(*msgs)


class EnvracDictFieldError(EnvracException):
    pass


class EnvracRangeError(EnvracException):
    def __init__(
        self,
        name: str,
        type: ValueType,
        value: str,
        min_val: Any,
        max_val: Any,
        print_value: bool = False,
    ):
        if not print_value:
            value = HIDDEN_VALUE
        msgs = [
            f'Value for environment variable "{name}" must be in range `{min_val}` - `{max_val}`.',
            f"Value: {value}",
        ]
        super().__init__(*msgs)


class EnvracParsingError(EnvracException):
    def __init__(
        self,
        name: str,
        type: ValueType,
        value: str,
        format_str: str | None = None,
        print_value: bool = False,
    ):
        if not print_value:
            value = HIDDEN_VALUE
        msgs = [
            f'Value for environment variable "{name}" could not be parsed to type `{type}`.',
            f"Value: {value}",
        ]
        if format_str:
            msgs.append(f"Try: {format_str}")
        super().__init__(*msgs)


class EnvracSpecificationError(EnvracException):
    def __init__(self, name: str, diff: str):
        msgs = [
            f'Environment variable "{name}" requested differently in multiple places.',
            f"Diff: {diff}",
        ]
        super().__init__(*msgs)


class EnvracUnsetVariableError(EnvracException):
    def __init__(self, name: str):
        super().__init__(f'Environment variable "{name}" must be set.')
