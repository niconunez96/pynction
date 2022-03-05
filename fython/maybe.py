from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from fython.either import Either, Left, Right

T = TypeVar("T")
V = TypeVar("V")
L = TypeVar("L")


class Maybe(ABC, Generic[T]):
    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def map(self, f: Callable[[T], V]) -> "Maybe[V]":
        raise NotImplementedError

    def get_or_else(self, default: T) -> T:
        raise NotImplementedError

    def to_either(self, error: L) -> Either[L, T]:
        raise NotImplementedError


class Nothing(Maybe[T]):
    def is_empty(self) -> bool:
        return True

    def map(self, _: Callable[[T], V]) -> Maybe[V]:
        return Nothing()

    def get_or_else(self, default: T) -> T:
        return default

    def to_either(self, error: L) -> Either[L, T]:
        return Left(error)


class Just(Maybe[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def is_empty(self) -> bool:
        return False

    def map(self, f: Callable[[T], V]) -> Maybe[V]:
        return Just(f(self.value))

    def get_or_else(self, _: T) -> T:
        return self.value

    def to_either(self, _: L) -> Either[L, T]:
        return Right(self.value)
