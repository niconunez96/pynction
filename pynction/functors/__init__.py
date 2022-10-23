from typing import Callable, Generic, TypeVar

from typing_extensions import Protocol

T_cov = TypeVar("T_cov", covariant=True)
T2 = TypeVar("T2")


class Functor(Generic[T_cov], Protocol):
    def map(self, f: Callable[[T_cov], T2]) -> "Functor[T2]":
        raise NotImplementedError
