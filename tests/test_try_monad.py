from unittest.mock import Mock

from pynction import try_of


class TestSuccess:
    def test_it_should_transform_content_of_success(self):
        example = try_of(lambda: 1)

        result = example.map(lambda s: s + 1).get_or_else_get(lambda _: 0)

        assert result == 2

    def test_it_should_return_value_when_ask_get_or_else_get(self):
        example = try_of(lambda: 1)

        result = example.get_or_else_get(lambda _: 0)

        assert result == 1

    def test_it_should_execute_on_success_callback(self):
        on_success = Mock()
        on_failure = Mock()
        example = try_of(lambda: 1)

        example.on(on_success, on_failure)

        on_success.assert_called_once_with(1)
        on_failure.assert_not_called()

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


class TestFailure:
    def test_it_should_return_default_value_provided(self):
        def f():
            raise Exception("Boom")

        example = try_of(f)

        result = example.map(lambda s: s + 1).get_or_else_get(lambda _: 0)

        assert result == 0

    def test_it_should_execute_on_failure_callback(self):
        on_success = Mock()
        on_failure = Mock()
        error = Exception("Boom")

        def f():
            raise error

        example = try_of(f)

        example.on(on_success, on_failure)

        on_failure.assert_called_once_with(error)
        on_success.assert_not_called()

    def test_it_should_execute_catch_statement(self):
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
