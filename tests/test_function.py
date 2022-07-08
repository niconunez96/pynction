from pynction import pynction0, pynction1, pynction2, pynction3, pynction4


@pynction1
def sum_10(arg: int) -> int:
    return arg + 10


@pynction2
def sum_two_numbers(x: int, y: int) -> int:
    return x + y


@pynction3
def sum_three_numbers(x: int, y: int, z: int) -> int:
    return x + y + z


@pynction4
def sum_four_numbers(x: int, y: int, z: int, q: int) -> int:
    return x + y + z + q


class TestProvider:

    obtain_number = pynction0(lambda: 10)

    def test_it_should_return_value_when_call_function(self):
        assert 10 == self.obtain_number()

    def test_it_should_compose_provider_with_function(self):
        assert 20 == (self.obtain_number | sum_10)()


class TestFunction:
    def test_it_should_return_value_when_call_function(self):
        assert 40 == sum_10(30)

    def test_it_should_compose_provider_with_function(self):
        sum_20 = sum_10 | sum_10
        assert 40 == sum_20(20)


class TestFunction2:
    def test_it_should_return_value_when_call_function(self):
        assert 80 == sum_two_numbers(30, 50)

    def test_it_should_compose_provider_with_function(self):
        sum_two_plus_10 = sum_two_numbers | sum_10
        assert 13 == sum_two_plus_10(1, 2)

    def test_it_should_transform_function2_to_function(self):
        curried_sum_two_numbers = sum_two_numbers.curried
        assert 20 == curried_sum_two_numbers(10)(10)


class TestFunction3:
    def test_it_should_return_value_when_call_function(self):
        assert 100 == sum_three_numbers(30, 50, 20)

    def test_it_should_compose_provider_with_function(self):
        sum_three_plus_20 = sum_three_numbers | sum_10 | sum_10
        assert 26 == sum_three_plus_20(1, 2, 3)

    def test_it_should_transform_function3_to_function(self):
        curried_sum_three_numbers = sum_three_numbers.curried
        assert 25 == curried_sum_three_numbers(10)(10)(5)


class TestFunction4:
    def test_it_should_return_value_when_call_function(self):
        assert 4 == sum_four_numbers(1, 1, 1, 1)

    def test_it_should_compose_provider_with_function(self):
        sum_four_plus_30 = sum_four_numbers | sum_10 | sum_10 | sum_10
        assert 34 == sum_four_plus_30(1, 1, 1, 1)

    def test_it_should_transform_function4_to_function(self):
        curried_sum_four_numbers = sum_four_numbers.curried
        assert 30 == curried_sum_four_numbers(10)(10)(5)(5)
