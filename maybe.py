from typing import Callable, Generic, TypeVar, Union

from either import Either, Left, Right


T = TypeVar("T")
V = TypeVar("V")
L = TypeVar("L")


class Nothing(Generic[T]):
    def is_empty(self) -> bool:
        return True

    def map(self, _: Callable[[T], V]) -> "Nothing":
        return self

    def get_or_else(self, default: T) -> T:
        return default

    def to_either(self, error: L) -> Either[L, T]:
        return Left(error)


class Just(Generic[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def is_empty(self) -> bool:
        return False

    def map(self, f: Callable[[T], V]) -> "Just[V]":
        return Just(f(self.value))

    def get_or_else(self, _: T) -> T:
        return self.value

    def to_either(self, _: L) -> Either[L, T]:
        return Right(self.value)


Maybe = Union[Nothing[T], Just[T]]


def isEmpty(something: Maybe[str]) -> bool:
    return something.map(lambda s: s.upper()).is_empty()


def sum10(something: Maybe[int]) -> int:
    return something.map(lambda a: a + 10).get_or_else(10)


def sum20(something: Maybe[int]) -> Either[str, int]:
    return something.map(lambda x: x + 20).to_either("NUMBER_NOT_FOUND")


print(isEmpty(Nothing()))
print(isEmpty(Just("something")))


print(sum10(Nothing()))
print(sum10(Just(10)))
