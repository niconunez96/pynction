from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Callable, Generator, Generic, Optional, TypeVar

from .either import Either, Left, Right

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)
L = TypeVar("L")


class Maybe(ABC, Generic[T]):
    @staticmethod
    def of(value: Optional[T]) -> "Maybe[T]":  # type: ignore
        return Nothing() if not value else Just(value)

    @abstractproperty
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def map(self, f: Callable[[T], V]) -> "Maybe[V]":
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, f: Callable[[T], "Maybe[V]"]) -> "Maybe[V]":
        raise NotImplementedError

    def get_or_else(self, default: T) -> T:  # type: ignore
        raise NotImplementedError

    def to_either(self, error: L) -> Either[L, T]:
        raise NotImplementedError


class Nothing(Maybe):
    _instance: Optional["Nothing"] = None

    def __str__(self) -> str:
        return "Nothing"

    @classmethod
    def get_instance(cls) -> "Nothing":
        if not cls._instance:
            cls._instance = Nothing()
        return cls._instance

    @property
    def is_empty(self) -> bool:
        return True

    def map(self, _: Callable[[Any], Any]) -> Maybe[Any]:
        return self.get_instance()

    def flat_map(self, _: Callable[[Any], "Maybe[Any]"]) -> "Maybe[Any]":
        return self.get_instance()

    def get_or_else(self, default: T) -> T:  # type: ignore
        return default

    def to_either(self, error: L) -> Either[L, Any]:
        return Left(error)


class Just(Maybe[T]):
    _value: T

    def __init__(self, value: T):
        self._value = value

    def __str__(self) -> str:
        return f"Just({self._value})"

    @property
    def is_empty(self) -> bool:
        return False

    def map(self, f: Callable[[T], V]) -> Maybe[V]:
        return Just(f(self._value))

    def flat_map(self, f: Callable[[T], "Maybe[V]"]) -> "Maybe[V]":
        return f(self._value)

    def get_or_else(self, _: T) -> T:  # type: ignore
        return self._value

    def to_either(self, _: L) -> Either[L, T]:
        return Right(self._value)


DoMaybe = Generator[Maybe[T], T, V]


def do(generator: Callable[..., DoMaybe[T, V]]) -> Callable[..., Maybe[V]]:
    def wrapper(*args):
        gen = generator(*args)
        maybe_monad = next(gen)
        while True:
            try:
                if type(maybe_monad) == Nothing:
                    return Nothing()
                maybe_monad = gen.send(maybe_monad._value)
            except StopIteration as e:
                return Just(e.value)

    return wrapper
