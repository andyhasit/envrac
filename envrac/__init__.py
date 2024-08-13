# flake8: noqa
from .envrac import env
from .exceptions import (
    EnvracChoiceError,
    EnvracDictFieldError,
    EnvracParsingError,
    EnvracRangeError,
    EnvracSpecificationError,
    EnvracUnsetVariableError,
)

VERSION = (0, 0, 2)
__version__ = ".".join(map(str, VERSION))
