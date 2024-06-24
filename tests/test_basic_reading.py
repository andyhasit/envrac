from typing import Any
import pytest

from envrac import EnvracUnsetVariableError, EnvracParsingError
from .type_mixins import (
    BoolMixin,
    DateMixin,
    DateTimeMixin,
    FloatMixin,
    IntMixin,
    StrMixin,
    TimeMixin,
)

VALID_NULL_STRINGS = ("NONE", "NULL", "none", "null", "noNe", "nuLL")


class BasicReadingTest:
    method: str = ""
    default_value: Any
    expected_value: Any
    other_value: Any
    unonvertible_value: Any
    choices: Any
    valid_choice: Any
    invalid_choice: Any
    min_val: Any
    too_low: Any
    max_val: Any
    too_high: Any
    goldilock: Any
    valid_strings: Any

    # remove
    test_unconvertible = True

    def call(self, env, *args, **kwargs):
        return getattr(env, self.method)(*args, **kwargs)

    def call_(self, env, *args, **kwargs):
        return getattr(env, self.method + "_")(*args, **kwargs)

    def test_reading_set_variable_with_default_returns_set_value(self, env, setvars):
        setvars(foo=self.expected_value)
        assert self.call(env, "foo", self.default_value) == self.expected_value

    def test_reading_set_variable_without_default_returns_set_value(self, env, setvars):
        setvars(foo=self.expected_value)
        assert self.call(env, "foo") == self.expected_value

    def test_reading_unset_variable_with_default_returns_default_value(
        self, env, setvars
    ):
        assert self.call(env, "foo", self.default_value) == self.default_value

    def test_reading_unset_variable_without_default_raises_error(self, env, setvars):
        with pytest.raises(EnvracUnsetVariableError):
            self.call(env, "foo")

    def test_reading_set_nullable_variable_with_default_returns_set_value(
        self, env, setvars
    ):
        setvars(foo=str(self.expected_value))
        assert self.call_(env, "foo", self.default_value) == self.expected_value

    def test_reading_set_nullable_variable_without_default_returns_set_value(
        self, env, setvars
    ):
        setvars(foo=self.expected_value)
        assert self.call_(env, "foo") == self.expected_value

    def test_reading_unset_nullable_variable_with_default_returns_default_value(
        self, env, setvars
    ):
        assert self.call_(env, "foo", self.default_value) == self.default_value

    def test_reading_unset_nullable_variable_without_default_raises_error(
        self, env, setvars
    ):
        with pytest.raises(EnvracUnsetVariableError):
            self.call_(env, "foo")

    def test_reading_nullable_unconvertible_type_raises_error(self, env, setvars):
        if self.unonvertible_value:
            setvars(foo=self.unonvertible_value)
            with pytest.raises(EnvracParsingError):
                self.call_(env, "foo")

    @pytest.mark.parametrize("value", VALID_NULL_STRINGS)
    def test_reading_nullable_variable_set_to_none_without_default_returns_none(
        self, env, value, setvars
    ):
        setvars(foo=value)
        assert self.call_(env, "foo") is None

    @pytest.mark.parametrize("value", VALID_NULL_STRINGS)
    def test_reading_nullable_variable_set_to_none_with_default_returns_none(
        self, env, value, setvars
    ):
        setvars(foo=value)
        assert self.call_(env, "foo", self.default_value) is None

    def test_with_prefix(self, env, setvars):
        setvars(FOO_A=self.expected_value, A=self.other_value)
        with env.prefix("FOO_"):
            assert self.call(env, "A") == self.expected_value
        assert self.call(env, "A") == self.other_value

    def test_error_during_prefix_context_reverts_prefix(self, env, setvars):
        setvars(BAR=self.expected_value)
        try:
            with env.prefix("FOO_"):
                self.call(env, "BAR")
        except EnvracUnsetVariableError:
            pass
        assert self.call(env, "BAR") == self.expected_value

    def test_reading_unconvertible_type_raises_error(self, env, setvars):
        if self.unonvertible_value:
            setvars(foo=self.unonvertible_value)
            with pytest.raises(EnvracParsingError):
                self.call(env, "foo")


class TestReadInt(IntMixin, BasicReadingTest):
    pass


class TestReadFloat(FloatMixin, BasicReadingTest):
    pass


class TestReadStr(StrMixin, BasicReadingTest):
    pass


class TestReadBool(BoolMixin, BasicReadingTest):
    pass


class TestReadDate(DateMixin, BasicReadingTest):
    pass


class TestReadDateTime(DateTimeMixin, BasicReadingTest):
    pass


class TestReadTime(TimeMixin, BasicReadingTest):
    pass
