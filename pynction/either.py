import abc
from typing import Callable, Generator, Generic, TypeVar

L = TypeVar("L")
L1 = TypeVar("L1")
R = TypeVar("R", covariant=True)
R1 = TypeVar("R1")


class Either(abc.ABC, Generic[L, R]):
    @staticmethod
    def right(value: R) -> "Either[L, R]":  # type: ignore
        return Right(value)

    @staticmethod
    def left(value: L) -> "Either[L, R]":
        return Left(value)

    @abc.abstractproperty
    def is_left(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def is_right(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, f: Callable[[R], R1]) -> "Either[L, R1]":
        raise NotImplementedError

    @abc.abstractmethod
    def filter_or_else(
        self, predicate: Callable[[R], bool], leftValue: L
    ) -> "Either[L, R]":
        raise NotImplementedError

    @abc.abstractmethod
    def get_or_else_get(self, f: Callable[[L], R]) -> R:
        raise NotImplementedError


class Right(Either[L, R]):
    _value: R

    def __init__(self, value: R):
        self._value = value

    def __str__(self) -> str:
        return f"Right({self._value})"

    @property
    def is_left(self) -> bool:
        return False

    @property
    def is_right(self) -> bool:
        return True

    def map(self, f: Callable[[R], R1]) -> Either[L, R1]:
        return Right(f(self._value))

    def filter_or_else(
        self, satisfyCondition: Callable[[R], bool], leftValue: L
    ) -> Either[L, R]:
        if satisfyCondition(self._value):
            return self
        else:
            return Left(leftValue)

    def get_or_else_get(self, _: Callable[[L], R]) -> R:
        return self._value


class Left(Either[L, R]):
    _value: L

    def __init__(self, value: L):
        self._value = value

    def __str__(self) -> str:
        return f"Left({self._value})"

    @property
    def is_left(self) -> bool:
        return True

    @property
    def is_right(self) -> bool:
        return False

    def map(self, _: Callable[[R], R1]) -> Either[L, R1]:
        return Left(self._value)

    def filter_or_else(self, _: Callable[[R], bool], _1: L) -> Either[L, R]:
        return self

    def get_or_else_get(self, f: Callable[[L], R]) -> R:
        return f(self._value)


DoEither = Generator[Either[L, R], R, R1]


def do(generator: Callable[..., DoEither[L, R, R1]]) -> Callable[..., Either[L, R1]]:
    def wrapper(*args):
        gen = generator(*args)
        either_monad = next(gen)
        while True:
            try:
                if type(either_monad) == Left:
                    return either_monad
                either_monad = gen.send(either_monad._value)
            except StopIteration as e:
                return Right(e.value)

    return wrapper
