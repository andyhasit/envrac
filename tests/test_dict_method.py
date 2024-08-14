class TestDictFieldParsing:

    def test_values_default_to_strings(self, env, setvars):
        setvars(foo="hello", bar=3)
        assert env.dict("foo", "bar") == {"foo": "hello", "bar": "3"}

    def test_with_type(self, env, setvars):
        setvars(foo=3)
        assert env.dict("foo:int") == {"foo": 3}

    def test_with_default(self, env, setvars):
        assert env.dict("foo=xyz") == {"foo": "xyz"}

    def test_with_type_and_default(self, env, setvars):
        assert env.dict("foo:int=45") == {"foo": 45}

    def test_read_nonee(self, env, setvars):
        setvars(foo="NULL")
        assert env.dict("?foo") == {"foo": None}

    def test_read_none_with_type(self, env, setvars):
        setvars(foo="NULL")
        assert env.dict("?foo:int") == {"foo": None}

    def test_read_none_with_default(self, env, setvars):
        setvars(foo="NULL")
        assert env.dict("?foo=xyz") == {"foo": None}

    def test_read_none_with_type_and_default(self, env, setvars):
        setvars(foo="NULL")
        assert env.dict("?foo:int=45") == {"foo": None}


class TestDictPrefixHandling:

    def test_with_prefix_keeps_prefix(self, env, setvars):
        setvars(x_foo=45, x_bar="hello")
        with env.prefix("x_"):
            assert env.dict("foo:int", "bar") == {"x_foo": 45, "x_bar": "hello"}

    def test_can_drop_prefix(self, env, setvars):
        setvars(x_foo=45, x_bar="hello")
        with env.prefix("x_"):
            assert env.dict("foo:int", "bar", drop_prefix=True) == {
                "foo": 45,
                "bar": "hello",
            }
