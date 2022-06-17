from typing import Union
from unittest.mock import Mock

import pytest

from pynction import DoEither, Either, do_either, left, right


class TestRight:
    def test_str_should_return_value(self):
        assert str(right(1)) == "Right(1)"

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
            lambda _: 0
        )

        assert result == 20

    def test_it_should_return_left_value_provided_when_not_satisfy_filter(self):
        example = right(20)

        result = example.filter_or_else(lambda a: a < 10, "ERROR").get_or_else_get(
            lambda _: 0
        )

        assert result == 0


class TestLeft:
    def test_str_should_return_value(self):
        assert str(left("ERROR")) == "Left(ERROR)"

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
        assert result._value == "ERROR"


# Do notation tests


@do_either
def example_with_nothing() -> DoEither[str, int, int]:
    x = yield right(1)
    y = yield left("error!")
    return x + y


@do_either
def example_with_nothing_2() -> DoEither[str, int, int]:
    v = yield right(5)
    x = yield right(1)
    y = yield left("error!")
    z = yield right(10)
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
def example_with_unexpected_exception() -> DoEither[str, str, str]:
    x = yield right("EXAMPLE")  # noqa: F841
    y = yield right("EXAMPLE")  # noqa: F841
    raise Exception("Unexpected exception")
    # return x + y


@do_either
def example_with_arguments(x: int, y: int) -> DoEither[str, int, int]:
    foo = yield right(10)
    return x + y + foo


@pytest.mark.parametrize(
    "do_notation_func", [example_with_nothing, example_with_nothing_2]
)
def test_do_notation_should_return_left_when_any_expression_return_a_left(
    do_notation_func,
):
    result = do_notation_func()

    assert result.is_left is True
    assert result._value == "error!"


@pytest.mark.parametrize(
    "do_notation_func, expected_result",
    [
        (example_with_return_value, 3),
        (example_with_return_value_2, "john wick with age 25"),
    ],
)
def test_do_notation_should_return_a_right_with_value_calculated(
    do_notation_func, expected_result
):
    result = do_notation_func()

    assert result.is_right is True
    assert result._value == expected_result


def test_do_notation_should_not_catch_unexpected_exceptions():
    with pytest.raises(Exception) as e:
        example_with_unexpected_exception()
        assert str(e) == "Unexpected exception"


def test_do_notation_should_pass_arguments():
    result = example_with_arguments(1, 2)

    assert result.is_right is True
    assert result._value == 13
