from unittest.mock import Mock

from pynction import try_of


class TestSuccess:
    def test_it_should_transform_content_of_success(self):
        example = try_of(lambda: 1)

        result = example.map(lambda s: s + 1)

        assert str(result) == "Success[2]"

    def test_it_should_return_success_value_when_unpack_it(self):
        example = try_of(lambda: 1)

        result = example.map(lambda s: s + 1).get_or_else_get(lambda _: 0)

        assert result == 2

    def test_it_should_return_failure_when_function_raises_exception(self):
        def explode() -> int:
            raise Exception("Boom!")

        example = try_of(lambda: 1)

        result = example.map(lambda value: explode())

        assert str(result) == "Failure[Exception('Boom!')]"

    def test_it_should_ignore_on_failure_consumer(self):
        on_success = None
        on_failure = Mock()
        example = try_of(lambda: 1)

        example.run(on_success, on_failure)

        on_failure.assert_not_called()

    def test_it_should_execute_on_success_consumer(self):
        on_success = Mock()
        on_failure = None
        example = try_of(lambda: 1)

        example.run(on_success, on_failure)

        on_success.assert_called_once_with(1)

    def test_it_should_ignore_catch_statement(self):
        catch_function = Mock()
        example = try_of(lambda: 1)

        example.catch(catch_function)

        catch_function.assert_not_called()

    def test_it_should_execute_and_finally_statement(self):
        finally_function = Mock()
        example = try_of(lambda: 1)

        example.and_finally(finally_function)

        finally_function.assert_called_once()

    def test_it_should_transform_success_to_either_right(self):
        example = try_of(lambda: 1)

        result = example.to_either()

        assert result.is_right is True
        assert str(result) == "Right[1]"

    def test_flat_map_should_return_success_with_new_value(
        self,
    ):
        example = try_of(lambda: 1)

        result = example.flat_map(lambda value: try_of(lambda: value + 50))

        assert str(result) == "Success[51]"

    def test_flat_map_should_return_failure_when_function_provided_throw_exception(
        self,
    ):
        example = try_of(lambda: 1)

        def explode():
            raise ValueError("Boom")

        result = example.flat_map(lambda value: try_of(explode))

        assert str(result) == "Failure[ValueError('Boom')]"


class TestFailure:
    def test_flat_map_should_return_failure_when_applied_to_failure(self):
        def explode() -> int:
            raise ValueError("Boom")

        example = try_of(explode)

        result = example.flat_map(lambda value: try_of(lambda: value + 100))

        assert str(result) == "Failure[ValueError('Boom')]"

    def test_it_should_return_default_value_provided(self):
        def f():
            raise IOError("Boom")

        def exc_handler(e: Exception) -> int:
            if isinstance(e, ValueError):
                return 10
            elif isinstance(e, IOError):
                return 20
            return 30

        example = try_of(f)

        result = example.map(lambda s: s + 1).get_or_else_get(exc_handler)

        assert result == 20

    def test_it_should_execute_on_failure_consumer(self):
        on_success = None
        on_failure = Mock()
        error = Exception("Boom")

        def f():
            raise error

        example = try_of(f)

        example.run(on_success, on_failure)

        on_failure.assert_called_once_with(error)

    def test_it_should_ignore_on_success_consumer(self):
        on_success = Mock()
        on_failure = None
        error = Exception("Boom")

        def f():
            raise error

        example = try_of(f)

        example.run(on_success, on_failure)

        on_success.assert_not_called()

    def test_it_should_return_failure_if_recover_function_raise_exception(self):
        def f() -> int:
            raise Exception("Boom")

        def recover() -> int:
            raise ValueError("🤯")

        example = try_of(f)

        result = example.catch(lambda exc: recover())

        assert str(result) == "Failure[ValueError('🤯')]"

    def test_it_should_return_success_after_recover_from_exception(self):
        def f():
            raise Exception("Boom")

        example = try_of(f)

        result = example.catch(lambda exc: -99).get_or_else_get(lambda _: 0)

        assert result == -99

    def test_it_should_execute_and_finally_statement(self):
        finally_function = Mock()

        def f():
            raise Exception("Boom")

        example = try_of(f)

        example.and_finally(finally_function)

        finally_function.assert_called_once()

    def test_it_should_transform_failure_to_either_left(self):
        def f():
            raise Exception("Boom")

        example = try_of(f)

        result = example.to_either()

        assert result.is_left is True
        assert str(result) == "Left[Boom]"
