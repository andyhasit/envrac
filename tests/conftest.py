import os
import pytest
from envrac import env as _env


@pytest.fixture
def env():
    """
    Use this fixture to reset `env` after the test has run.
    """
    yield _env
    _env.reset()


@pytest.fixture
def setvars():
    """
    Use this fixture to set environment variables in a test.
    They will be deleted after the test has run.
    """
    vars_set = []

    def _setvars(**kwargs):
        for name, value in kwargs.items():
            os.environ[name] = str(value)
            vars_set.append(name)

    yield _setvars
    for name in vars_set:
        del os.environ[name]
