import pytest
from envrac import EnvracSpecificationError


class TestVarSpecficationUniqueness:

    def test_changing_default_raises_error(self, env, setvars):
        setvars(BAR="hello")
        with pytest.raises(EnvracSpecificationError):
            env.str("BAR", default="abc")
            env.str("BAR", default="def")

    def test_changing_read_none_raises_error(self, env, setvars):
        setvars(BAR="hello")
        with pytest.raises(EnvracSpecificationError):
            env.str("BAR")
            env.str("BAR", read_none=True)

    def test_changing_type_raises_error(self, env, setvars):
        setvars(BAR="77")
        with pytest.raises(EnvracSpecificationError):
            env.int("BAR")
            env.str("BAR")

    def test_changing_choices_raises_error(self, env, setvars):
        setvars(BAR="2")
        with pytest.raises(EnvracSpecificationError):
            env.int("BAR", choices=[1, 2, 3])
            env.int("BAR", choices=[1, 2, 3, 4])

    def test_changing_min_value_raises_error(self, env, setvars):
        setvars(BAR="2")
        with pytest.raises(EnvracSpecificationError):
            env.int("BAR", min_val=1)
            env.int("BAR", min_val=0)

    def test_changing_max_value_raises_error(self, env, setvars):
        setvars(BAR="2")
        with pytest.raises(EnvracSpecificationError):
            env.int("BAR", max_val=3)
            env.int("BAR", max_val=4)
