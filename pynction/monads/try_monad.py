from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .either import Either, Left, Right

T = TypeVar("T")
S = TypeVar("S")


class Try(ABC, Generic[T]):
    @staticmethod
    def of(f: Callable[[], T]) -> "Try[T]":
        try:
            result = f()
            return Success(result)
        except Exception as e:
            return Failure(e)

    @abstractmethod
    def map(self, f: Callable[[T], S]) -> "Try[S]":
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, f: Callable[[T], "Try[S]"]) -> "Try[S]":
        raise NotImplementedError

    @abstractmethod
    def get_or_else_get(self, default: Callable[[Exception], T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def on(
        self,
        on_success: Callable[[T], None] = None,
        on_failure: Callable[[Exception], None] = None,
    ) -> "Try[T]":
        raise NotImplementedError

    @abstractmethod
    def catch(self, f: Callable[[Exception], T]) -> "Try[T]":
        raise NotImplementedError

    def and_finally(self, f: Callable[[], None]) -> "Try[T]":
        f()
        return self

    @abstractmethod
    def to_either(self) -> Either[Exception, T]:
        raise NotImplementedError


@dataclass(frozen=True)
class Failure(Try[T]):
    _e: Exception

    def map(self, _: Callable[[T], S]) -> "Try[S]":
        return Failure(self._e)

    def flat_map(self, _: Callable[[T], "Try[S]"]) -> "Try[S]":
        return Failure(self._e)

    def get_or_else_get(self, default: Callable[[Exception], T]) -> T:
        return default(self._e)

    def on(
        self,
        _: Callable[[T], None] = None,
        on_failure: Callable[[Exception], None] = None,
    ) -> "Try[T]":
        if on_failure:
            on_failure(self._e)
        return self

    def catch(self, f: Callable[[Exception], T]) -> "Try[T]":
        try:
            return Success(f(self._e))
        except Exception as e:
            return Failure(e)

    def to_either(self) -> Either[Exception, T]:
        return Left(self._e)


@dataclass(frozen=True)
class Success(Try[T]):
    _value: T

    def map(self, f: Callable[[T], S]) -> "Try[S]":
        try:
            return Success(f(self._value))
        except Exception as e:
            return Failure(e)

    def flat_map(self, f: Callable[[T], "Try[S]"]) -> "Try[S]":
        try:
            return f(self._value)
        except Exception as e:
            return Failure(e)

    def get_or_else_get(self, _: Callable[[Exception], T]) -> T:
        return self._value

    def on(
        self,
        on_success: Callable[[T], None] = None,
        _: Callable[[Exception], None] = None,
    ) -> "Try[T]":
        if on_success:
            on_success(self._value)
        return self

    def catch(self, _: Callable[[Exception], T]) -> "Try[T]":
        return self

    def to_either(self) -> Either[Exception, T]:
        return Right(self._value)
