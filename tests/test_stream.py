import pytest

from pynction.streams.stream import stream, stream_of


class TestStream:
    def test_it_should_create_stream_from_list(self):
        example_stream = stream_of([1, 2, 3, 4])

        assert example_stream.to_list() == [1, 2, 3, 4]

    @pytest.mark.parametrize(
        "iterator_example, expected_value",
        [
            (range(1, 10), [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            (range(1, 10, 2), [1, 3, 5, 7, 9]),
            ((e for e in [1, 2, 3]), [1, 2, 3]),
        ],
    )
    def test_it_should_create_stream_from_iterator(
        self, iterator_example, expected_value
    ):
        example_stream = stream_of(iterator_example)

        assert example_stream.to_list() == expected_value

    def test_it_should_create_stream_from_set(self):
        example_stream = stream_of({1, 2, 3, 4})

        assert example_stream.to_list() == [1, 2, 3, 4]

    def test_it_should_create_stream_from_generator(self):
        def example_generator():
            yield 1
            yield 2
            yield 3

        example_stream = stream_of(example_generator())

        assert example_stream.to_list() == [1, 2, 3]

    def test_it_should_create_stream_from_multiple_args(self):
        example_stream = stream(1, 2, 3, 4, 5)

        assert example_stream.to_list() == [1, 2, 3, 4, 5]

    def test_it_should_transform_elements_of_stream(self):
        example_stream = stream(1, 2, 3, 4, 5)

        doubled_numbers = example_stream.map(lambda x: x * 2)

        assert doubled_numbers.to_list() == [2, 4, 6, 8, 10]

    def test_it_should_filter_elements_of_stream(self):
        example_stream = stream(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

        even_numbers = example_stream.filter(lambda x: x % 2 == 0)

        assert even_numbers.to_list() == [2, 4, 6, 8, 10]

    def test_it_should_transform_and_flatten_elements_of_stream(self):
        example_stream = stream(1, 2, 3, 4)

        doubled_and_tripled = example_stream.flat_map(lambda x: [x * 2, x * 3])

        assert doubled_and_tripled.to_list() == [2, 3, 4, 6, 6, 9, 8, 12]

    def test_it_should_return_elements_until_condition_is_not_satisfied(self):
        example_stream = stream_of(range(1, 20))

        less_than_ten = example_stream.take_while(lambda x: x < 10)

        assert less_than_ten.to_list() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_it_should_convert_elements_to_set(self):
        example_stream = stream(1, 1, 1, 1, 1, 1, 1, 2, 2, 2)

        assert example_stream.to_set() == {1, 2}

    def test_stream_should_be_iterable(self):
        example_stream = stream(1, 2, 3, 4)

        assert list(example_stream) == [1, 2, 3, 4]
