from pynction.maybe import Just, Nothing, Maybe


class TestMaybe:
    def test_it_should_return_just_when_value_is_not_none(self):
        assert type(Maybe.of(1)) == Just

    def test_it_should_return_nothing_when_value_is_none(self):
        assert type(Maybe.of(None)) == Nothing


class TestJust:
    def test_it_should_transform_content_of_just(self):
        example = Just("EXAMPLE")

        result = example.map(lambda s: s.lower()).get_or_else("")

        assert result == "example"

    def test_it_should_return_false_when_ask_if_is_empty(self):
        example = Just("EXAMPLE")

        assert example.is_empty is False


class TestNothing:
    def test_it_should_return_default_value_passed(self):
        example = Nothing()

        result = example.get_or_else("default")

        assert result == "default"

    def test_it_should_return_true_when_ask_if_is_empty(self):
        example = Nothing()

        assert example.is_empty is True
