from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, NoReturn, Optional, TypeVar, cast

from typing_extensions import ParamSpec

from .either import Either, Left, Right

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)
L = TypeVar("L")


class Maybe(ABC, Generic[T]):
    @staticmethod
    def of(value: Optional[T]) -> "Maybe[T]":
        return Nothing.get_instance() if not value else Just(value)

    @staticmethod
    def nothing() -> "Nothing":
        return Nothing.get_instance()

    @staticmethod
    def just(value: T) -> "Just[T]":  # type: ignore
        return Just(value)

    @abstractproperty
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def map(self, f: Callable[[T], V]) -> "Maybe[V]":
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, f: Callable[[T], "Maybe[V]"]) -> "Maybe[V]":
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: T) -> T:  # type: ignore
        raise NotImplementedError

    @abstractmethod
    def get_or_raise(self, error: Exception) -> T:
        raise NotImplementedError

    @abstractmethod
    def to_either(self, error: L) -> Either[L, T]:
        raise NotImplementedError


@dataclass
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

    def get_or_raise(self, error: Exception) -> NoReturn:
        raise error

    def to_either(self, error: L) -> Either[L, Any]:
        return Left(error)


@dataclass(frozen=True)
class Just(Maybe[T]):
    _value: T

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

    def get_or_raise(self, _: Exception) -> T:
        return self._value

    def to_either(self, _: L) -> Either[L, T]:
        return Right(self._value)


DoMaybe = Generator[Maybe[T], T, V]
P = ParamSpec("P")


def do(generator: Callable[P, DoMaybe[T, V]]) -> Callable[P, Maybe[V]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Maybe[V]:
        gen = generator(*args, **kwargs)
        maybe_monad = next(gen)
        while True:
            try:
                if type(maybe_monad) == Nothing:
                    return Nothing()
                maybe_monad = gen.send(cast(Just, maybe_monad)._value)
            except StopIteration as e:
                return Just(e.value)

    return wrapper
