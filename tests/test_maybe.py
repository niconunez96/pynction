from typing import Union

import pytest

from pynction.maybe import DoMaybe, Just, Maybe, Nothing, do


class TestMaybe:
    def test_it_should_return_just_when_value_is_not_none(self):
        assert type(Maybe.of(1)) == Just

    def test_it_should_return_nothing_when_value_is_none(self):
        assert type(Maybe.of(None)) == Nothing


class TestJust:
    def test_str_should_return_value(self):
        assert str(Just(1)) == "Just(1)"

    def test_it_should_transform_content_of_just(self):
        example = Just("EXAMPLE")

        result = example.map(lambda s: s.lower()).get_or_else("")

        assert result == "example"

    def test_it_should_return_false_when_ask_if_is_empty(self):
        example = Just("EXAMPLE")

        assert example.is_empty is False

    def test_it_should_return_either_right_with_value(self):
        example = Just("EXAMPLE")

        result = example.to_either("error")

        assert result._value == "EXAMPLE"

    def test_it_should_return_just_when_apply_flat_map(self):
        foo = Just(1)

        result = foo.flat_map(lambda a: Just(a + 5))

        assert result.is_empty is False
        assert result._value == 6


class TestNothing:
    def test_str_should_return_value(self):
        assert str(Nothing()) == "Nothing"

    def test_it_should_return_default_value_passed(self):
        example = Nothing()

        result = example.map(lambda a: a + 1).get_or_else("default")

        assert result == "default"

    def test_it_should_return_true_when_ask_if_is_empty(self):
        example = Nothing()

        assert example.is_empty is True

    def test_it_should_return_either_left_with_error(self):
        example = Nothing()

        result = example.to_either("error")

        assert result._value == "error"

    def test_flat_map_should_return_nothing_when_applied_to_nothing(self):
        foo = Nothing()
        bar = foo.flat_map(lambda a: Just(a + 1))

        assert bar.is_empty is True

    def test_flat_map_should_return_nothing_when_expression_returns_nothing(self):
        foo = Just(1)
        bar = foo.flat_map(lambda a: Nothing())

        assert bar.is_empty is True


# Do notation tests


@do
def example_with_nothing() -> DoMaybe[int, int]:
    x = yield Just(1)
    y = yield Nothing()
    return x + y


@do
def example_with_nothing_2() -> DoMaybe[int, int]:
    v = yield Just(5)
    x = yield Just(1)
    y = yield Nothing()
    z = yield Just(10)
    return v + x + y + z


@do
def example_with_return_value() -> DoMaybe[int, int]:
    x = yield Just(1)
    y = yield Just(2)
    return x + y


@do
def example_with_return_value_2() -> DoMaybe[Union[int, str], str]:
    name = yield Just("nicolas")
    age = yield Just(25)
    lastname = yield Just("nunez")
    return f"{name} {lastname} with age {age}"


@do
def example_with_unexpected_exception() -> DoMaybe[str, str]:
    x = yield Just("EXAMPLE")  # noqa: F841
    y = yield Just("EXAMPLE")  # noqa: F841
    raise Exception("Unexpected exception")
    # return x + y


@do
def example_with_arguments(x: int, y: int) -> DoMaybe[int, int]:
    foo = yield Just(10)
    return x + y + foo


@pytest.mark.parametrize(
    "do_notation_func", [example_with_nothing, example_with_nothing_2]
)
def test_do_notation_should_return_nothing_when_any_expression_return_a_nothing(
    do_notation_func,
):
    result = do_notation_func()

    assert result.is_empty is True


@pytest.mark.parametrize(
    "do_notation_func, expected_result",
    [
        (example_with_return_value, 3),
        (example_with_return_value_2, "nicolas nunez with age 25"),
    ],
)
def test_do_notation_should_return_a_just_with_value_calculated(
    do_notation_func, expected_result
):
    result = do_notation_func()

    assert result.is_empty is False
    assert result._value == expected_result


def test_do_notation_should_not_catch_unexpected_exceptions():
    with pytest.raises(Exception) as e:
        example_with_unexpected_exception()
        assert str(e) == "Unexpected exception"


def test_do_notation_should_pass_arguments():
    result = example_with_arguments(1, 2)

    assert result.is_empty is False
    assert result._value == 13
