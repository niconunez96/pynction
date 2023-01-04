from typing import Any, Callable, Tuple, Union
from unittest.mock import Mock

import pytest
from typing_extensions import Literal

from pynction import DoEither, Either, _e, do_either, left, right
from pynction.monads.either import DoEitherN


class TestRight:
    def test_str_should_return_value(self):
        assert str(right(1)) == "Right[1]"

    def test_it_should_return_true_when_ask_if_is_right(self):
        assert right(1).is_right is True

    def test_it_should_return_false_when_ask_if_is_left(self):
        assert right(1).is_left is False

    def test_it_should_transform_content_of_right(self):
        example = right(1)

        result = example.map(lambda a: a + 1).get_or_else_get(lambda _: 0)

        assert result == 2

    def test_it_should_return_same_value_when_satisfy_filter(self):
        example = right(20)

        result = example.filter_or_else(lambda a: a > 10, "ERROR").get_or_else_get(
            lambda _: 0,
        )

        assert result == 20

    def test_it_should_return_left_value_provided_when_not_satisfy_filter(self):
        example = right(20)

        result = example.filter_or_else(lambda a: a < 10, "ERROR").get_or_else_get(
            lambda _: 0,
        )

        assert result == 0

    def test_it_should_return_the_same_right_value_when_try_to_recover(self):
        example: Either[str, int] = right(20)

        result = example.recover(lambda: 10)

        assert str(result) == "Right[20]"

    def test_it_should_run_provided_function_when_call_on_right(self):
        on_right_function = Mock()
        example: Either[str, int] = right(20)

        example.on_right(on_right_function)

        on_right_function.assert_called_once()

    def test_it_should_run_provided_function_when_call_run(self):
        on_right_function = Mock()
        on_left_function = Mock()
        example: Either[str, int] = right(20)

        example.run(
            on_right=on_right_function,
            on_left=on_left_function,
        )

        on_right_function.assert_called_once_with(20)
        on_left_function.assert_not_called()

    def test_it_should_not_run_provided_function_when_call_on_left(self):
        on_right_function = Mock()
        example: Either[str, int] = right(20)

        example.on_left(on_right_function)

        on_right_function.assert_not_called()


class TestLeft:
    def test_str_should_return_value(self):
        assert str(left("ERROR")) == "Left[ERROR]"

    def test_it_should_return_true_when_ask_if_is_left(self):
        assert left("ERROR").is_left is True

    def test_it_should_return_false_when_ask_if_is_right(self):
        assert left("ERROR").is_right is False

    def test_it_should_return_default_value_provided(self):
        example = left("ERROR")

        result = example.get_or_else_get(lambda _: 0)

        assert result == 0

    def test_it_should_ignore_map(self):
        example = left("ERROR")
        map_function = Mock()

        result = example.map(map_function).get_or_else_get(lambda _: 0)

        map_function.assert_not_called()
        assert result == 0

    def test_it_should_ignore_filter(self):
        example = left("ERROR")
        filter_function = Mock()

        result = example.filter_or_else(filter_function, "filter failed")

        filter_function.assert_not_called()
        assert str(result) == "Left[ERROR]"

    def test_it_should_return_function_value_when_try_to_recover(self):
        example: Either[str, int] = left("boom!")

        result = example.recover(lambda: 20)

        assert str(result) == "Right[20]"

    def test_it_should_return_function_value_using_error_when_try_to_recover(self):
        example: Either[str, int] = left("boom!")

        result = example.recover(lambda error: 10 if error == "boom!" else -1)

        assert str(result) == "Right[10]"

    def test_it_should_run_provided_function_when_call_on_left(self):
        on_left_function = Mock()
        example: Either[str, int] = left("boom!")

        example.on_left(on_left_function)

        on_left_function.assert_called_once()

    def test_it_should_run_provided_function_when_call_run(self):
        on_left_function = Mock()
        on_right_function = Mock()
        example: Either[str, int] = left("boom!")

        example.run(
            on_left=on_left_function,
            on_right=on_right_function,
        )

        on_left_function.assert_called_once_with("boom!")
        on_right_function.assert_not_called()

    def test_it_should_not_run_provided_function_when_call_on_right(self):
        on_left_function = Mock()
        example: Either[str, int] = left("boom!")

        example.on_right(on_left_function)

        on_left_function.assert_not_called()


# Do notation tests


@do_either
def example_with_left() -> DoEither[str, int, int]:
    x = yield right(1)
    y = yield left("error!")
    return x + y


@do_either
def example_with_left_2() -> DoEither[str, int, int]:
    v = yield right(5)
    x = yield right(1)
    y = yield left("error!")
    z = yield right(10)
    return v + x + y + z


@do_either
def dynamic_typing_returning_left() -> DoEitherN[str, int]:
    v = yield from _e(right(5))
    x = yield from _e(right(1))
    y = yield from _e(left("error!"))
    z = yield from _e(right(10))
    return v + x + y + z


@do_either
def example_with_return_value() -> DoEither[str, int, int]:
    x = yield right(1)
    y = yield right(2)
    return x + y


@do_either
def example_with_return_value_2() -> DoEither[str, Union[int, str], str]:
    def get_name() -> Either[str, str]:
        return right("john")

    name = yield get_name()
    age = yield right(25)
    lastname = yield right("wick")
    return f"{name} {lastname} with age {age}"


@do_either
def dynamic_typing_returning_value() -> DoEitherN[
    Literal["error", "ERROR1"],
    Tuple[int, str],
]:
    x = yield from _e(right(2))
    y = yield from _e(right(6))
    z = yield from _e(right("something"))
    return x + y, z


@do_either
def example_with_unexpected_exception() -> DoEither[str, str, str]:
    x = yield right("EXAMPLE")  # noqa: F841
    y = yield right("EXAMPLE")  # noqa: F841
    raise Exception("Unexpected exception")
    # return x + y


@do_either
def dynamic_typing_with_unexpected_exception() -> DoEitherN[str, str]:
    x = yield right("EXAMPLE")  # noqa: F841
    y = yield right("EXAMPLE")  # noqa: F841
    raise Exception("Unexpected exception")
    # return x + y


@do_either
def example_with_arguments(x: int, y: int) -> DoEither[str, int, int]:
    foo = yield right(10)
    return x + y + foo


@pytest.mark.parametrize(
    "do_notation_func",
    [example_with_left, example_with_left_2, dynamic_typing_returning_left],
)
def test_do_notation_should_return_left_when_any_expression_return_a_left(
    do_notation_func: Callable[[], Either[Any, Any]],
):
    result = do_notation_func()

    assert result.is_left is True
    assert str(result) == "Left[error!]"


@pytest.mark.parametrize(
    "do_notation_func, expected_result",
    [
        (example_with_return_value, 3),
        (example_with_return_value_2, "john wick with age 25"),
        (dynamic_typing_returning_value, (8, "something")),
    ],
)
def test_do_notation_should_return_a_right_with_value_calculated(
    do_notation_func: Callable[[], Either[Any, Any]],
    expected_result,
):
    result = do_notation_func()

    assert result.is_right is True
    assert str(result) == f"Right[{expected_result}]"


@pytest.mark.parametrize(
    "do_notation_func",
    [example_with_unexpected_exception, dynamic_typing_with_unexpected_exception],
)
def test_do_notation_should_not_catch_unexpected_exceptions(do_notation_func):
    with pytest.raises(Exception) as e:
        do_notation_func()
    assert str(e.value) == "Unexpected exception"


def test_do_notation_should_pass_arguments():
    result = example_with_arguments(1, 2)

    assert result.is_right is True
    assert str(result) == "Right[13]"
