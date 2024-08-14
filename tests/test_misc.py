# TODO: test_discovery
import os


def test_put_saves_var(env):
    env.put("foo", 21)
    assert os.environ["foo"] == "21"


def test_put_none_deletse_var(env):
    env.put("foo", 21)
    assert os.environ["foo"] == "21"
    env.put("foo", None)
    assert "foo" not in os.environ
