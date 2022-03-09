from unittest.mock import Mock
from pynction.either import Either, Left, Right


class TestEither:
    def test_it_should_return_right_with_specified_value(self):
        assert type(Either.right(1)) == Right

    def test_it_should_return_left_with_specified_value(self):
        assert type(Either.left("ERROR")) == Left


class TestRight:
    def test_it_should_return_true_when_ask_if_is_right(self):
        assert Right(1).is_right is True

    def test_it_should_return_false_when_ask_if_is_left(self):
        assert Right(1).is_left is False

    def test_it_should_transform_content_of_right(self):
        example = Right(1)

        result = example.map(lambda a: a + 1).get_or_else_get(lambda _: 0)

        assert result == 2

    def test_it_should_return_same_value_when_satisfy_filter(self):
        example = Right(20)

        result = example.filter_or_else(lambda a: a > 10, "ERROR").get_or_else_get(
            lambda _: 0
        )

        assert result == 20

    def test_it_should_return_left_value_provided_when_not_satisfy_filter(self):
        example = Right(20)

        result = example.filter_or_else(lambda a: a < 10, "ERROR").get_or_else_get(
            lambda _: 0
        )

        assert result == 0


class TestLeft:
    def test_it_should_return_true_when_ask_if_is_left(self):
        assert Left("ERROR").is_left is True

    def test_it_should_return_false_when_ask_if_is_right(self):
        assert Left("ERROR").is_right is False

    def test_it_should_return_default_value_provided(self):
        example = Left("ERROR")

        result = example.get_or_else_get(lambda _: 0)

        assert result == 0

    def test_it_should_ignore_map(self):
        example = Left("ERROR")
        map_function = Mock()

        result = example.map(map_function).get_or_else_get(lambda _: 0)

        map_function.assert_not_called()
        assert result == 0

    def test_it_should_ignore_filter(self):
        example = Left("ERROR")
        filter_function = Mock()

        result = example.map(filter_function).get_or_else_get(lambda _: 0)

        filter_function.assert_not_called()
        assert result == 0
