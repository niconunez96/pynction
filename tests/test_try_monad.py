from unittest.mock import Mock

from pynction.try_monad import Failure, Success, Try


class TestTry:
    def test_it_should_create_success_monad_when_function_does_not_raise_exception(
        self,
    ):
        def f():
            return 1

        assert type(Try.of(f)) == Success

    def test_it_should_create_failure_monad_when_function_does_not_raise_exception(
        self,
    ):
        def f():
            raise Exception()

        assert type(Try.of(f)) == Failure


class TestSuccess:
    def test_it_should_transform_content_of_success(self):
        example = Success(1)

        result = example.map(lambda s: s + 1).get_or_else_get(lambda _: 0)

        assert result == 2

    def test_it_should_return_value_when_ask_get_or_else_get(self):
        example = Success(1)

        result = example.get_or_else_get(lambda _: 0)

        assert result == 1

    def test_it_should_execute_on_success_callback(self):
        on_success = Mock()
        on_failure = Mock()
        example = Success(1)

        example.on(on_success, on_failure)

        on_success.assert_called_once_with(1)
        on_failure.assert_not_called()

    def test_it_should_ignore_catch_statement(self):
        catch_function = Mock()
        example = Success(1)

        example.catch(catch_function)

        catch_function.assert_not_called()

    def test_it_should_execute_and_finally_statement(self):
        finally_function = Mock()
        example = Success(1)

        example.and_finally(finally_function)

        finally_function.assert_called_once()

    def test_it_should_transform_success_to_either_right(self):
        example = Success(1)

        result = example.to_either()

        assert result.is_right is True


class TestFailure:
    def test_it_should_return_default_value_provided(self):
        example = Failure(Exception("Boom"))

        result = example.map(lambda s: s + 1).get_or_else_get(lambda _: 0)

        assert result == 0

    def test_it_should_execute_on_failure_callback(self):
        on_success = Mock()
        on_failure = Mock()
        error = Exception("Boom")
        example = Failure(error)

        example.on(on_success, on_failure)

        on_failure.assert_called_once_with(error)
        on_success.assert_not_called()

    def test_it_should_execute_catch_statement(self):
        example = Failure(Exception("Boom"))

        result = example.catch(lambda exc: -99).get_or_else_get(lambda _: 0)

        assert result == -99

    def test_it_should_execute_and_finally_statement(self):
        finally_function = Mock()
        example = Failure(Exception("Boom"))

        example.and_finally(finally_function)

        finally_function.assert_called_once()

    def test_it_should_transform_failure_to_either_left(self):
        example = Failure(Exception("Boom"))

        result = example.to_either()

        assert result.is_left is True
