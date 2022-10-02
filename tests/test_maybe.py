from typing import Union

import pytest

from pynction import DoMaybe, do_maybe, maybe, nothing


class TestJust:
    def test_str_should_return_value(self):
        assert str(maybe(1)) == "Just(1)"

    def test_it_should_transform_content_of_just(self):
        example = maybe("EXAMPLE")

        result = example.map(lambda s: s.lower()).get_or_else("")

        assert result == "example"

    def test_it_should_return_false_when_ask_if_is_empty(self):
        example = maybe("EXAMPLE")

        assert example.is_empty is False

    def test_it_should_return_either_right_with_value(self):
        example = maybe("EXAMPLE")

        result = example.to_either("error")

        assert result._value == "EXAMPLE"

    def test_it_should_return_just_when_apply_flat_map(self):
        foo = maybe(1)

        result = foo.flat_map(lambda a: maybe(a + 5))

        assert result.is_empty is False
        assert result._value == 6

    def test_it_should_return_element_when_call_get_or_raise(self):
        foo = maybe(1)

        assert 1 == foo.get_or_raise(Exception())


class TestNothing:
    def test_str_should_return_value(self):
        assert str(nothing) == "Nothing"

    def test_it_should_return_default_value_passed(self):
        example = nothing

        result = example.map(lambda a: a + 1).get_or_else("default")

        assert result == "default"

    def test_it_should_return_true_when_ask_if_is_empty(self):
        example = nothing

        assert example.is_empty is True

    def test_it_should_return_either_left_with_error(self):
        example = nothing

        result = example.to_either("error")

        assert result._value == "error"

    def test_flat_map_should_return_nothing_when_applied_to_nothing(self):
        foo = nothing
        bar = foo.flat_map(lambda a: maybe(a + 1))

        assert bar.is_empty is True

    def test_flat_map_should_return_nothing_when_expression_returns_nothing(self):
        foo = maybe(1)
        bar = foo.flat_map(lambda a: nothing)

        assert bar.is_empty is True

    def test_it_should_raise_exception_when_call_get_or_raise(self):
        foo = nothing

        with pytest.raises(AttributeError):
            foo.get_or_raise(AttributeError())


# Do notation tests


@do_maybe
def example_with_nothing() -> DoMaybe[int, int]:
    x = yield maybe(1)
    y = yield nothing
    return x + y


@do_maybe
def example_with_nothing_2() -> DoMaybe[int, int]:
    v = yield maybe(5)
    x = yield maybe(1)
    y = yield nothing
    z = yield maybe(10)
    return v + x + y + z


@do_maybe
def example_with_return_value() -> DoMaybe[int, int]:
    x = yield maybe(1)
    y = yield maybe(2)
    return x + y


@do_maybe
def example_with_return_value_2() -> DoMaybe[Union[int, str], str]:
    name = yield maybe("nicolas")
    age = yield maybe(25)
    lastname = yield maybe("nunez")
    return f"{name} {lastname} with age {age}"


@do_maybe
def example_with_unexpected_exception() -> DoMaybe[str, str]:
    x = yield maybe("EXAMPLE")  # noqa: F841
    y = yield maybe("EXAMPLE")  # noqa: F841
    raise Exception("Unexpected exception")
    # return x + y


@do_maybe
def example_with_arguments(x: int, y: int) -> DoMaybe[int, int]:
    foo = yield maybe(10)
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
