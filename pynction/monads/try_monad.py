from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from pynction.monads.either import Either, Left, Right

T = TypeVar("T")
S = TypeVar("S")


class Try(ABC, Generic[T]):
    """
    Try monad is the representation of the `try - except` statement.
    You can operate with function that raise exception in a functional way
    """

    @staticmethod
    def of(f: Callable[[], T]) -> "Try[T]":
        """
        Factory method that creates a `Success` if the function returns
        a value and returns a `Failure` if the function raises some exception.
        """
        try:
            result = f()
            return Success(result)
        except Exception as e:
            return Failure(e)

    @abstractmethod
    def map(self, f: Callable[[T], S]) -> "Try[S]":
        """
        If it is a `Success` instance, this method applies the `f` function over the value
        and:
        * Returns `Failure` if the operation raise an Exception, else
        * Returns the result wrapped in a `Success` instance.

        For `Failure` instances the `f` function is ignored.

        Example:
        ```
        try_of(lambda: 15).map(lambda a: a + 1)  # Returns Success(16)

        def boom():
            raise Exception
        try_of(boom).map(lambda a: a + 1)  # Returns Failure(Exception)
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, f: Callable[[T], "Try[S]"]) -> "Try[S]":
        """
        If it is a `Success` instance, this method applies the `f` function over the value
        and returns the `Try` instance returned by `f`.
        For `Failure` instances the `f` function is ignored.

        The difference with map is that the `f` function returns another `Try[V]` instead of plain `V`

        Example:
        ```
        try_of(lambda: 1).flat_map(lambda a: try_of(lambda a: a + 1))  # Returns Success(2)

        def boom():
            raise Exception
        try_of(boom).flat_map(lambda a: try_of(lambda a: a + 1))  # Returns Failure(Exception)
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def get_or_else_get(self, default: Callable[[Exception], T]) -> T:
        """
        * Returns value if it's a `Success` instance
        * Returns result of `default` if it's a `Failure` instance
        """
        raise NotImplementedError

    @abstractmethod
    def on(
        self,
        on_success: Callable[[T], None] = None,
        on_failure: Callable[[Exception], None] = None,
    ) -> "Try[T]":
        """
        Applies:
        * `on_success` if it's a `Success` instance
        * `on_failure` if it's a `Failure` instance

        Both functions should not return anything, this method should be used
        for running "impure" operations over `Try` instance.

        Example
        ```
        try_of(lambda: 1).on(on_success=lambda a: print(a))  # prints 1

        def boom():
            raise Exception("BOOM")
        try_of(boom).on(on_failure=lambda err: print(str(err)))  # prints "BOOM"
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def catch(self, f: Callable[[Exception], T]) -> "Try[T]":
        """
        If it is a `Failure` instance, this method applies the `f` function over the exception
        and:
        * Returns the result wrapped in a `Success` instance, else
        * Returns `Failure` again if `f` raises an Exception.

        For `Success` instances the `f` function is ignored.

        Example:
        ```
        try_of(lambda: 15).catch(lambda a: a + 1)  # Returns Success(15)

        def boom() -> int:
            raise Exception
        try_of(boom).catch(lambda err: 1)  # Returns Success(1)
        ```
        """
        raise NotImplementedError

    def and_finally(self, f: Callable[[], None]) -> "Try[T]":
        """
        This methods always applies the function `f`.
        It should be executed at the end of the `Try`.

        Example
        ```
        # Regular try catch
        try:
            db.open_session()
            db.insert(user)
        except:
            db.rollback()
        finally:
            db.close_session()

        # Try monad
        def insert(user: User) -> None:
            db.open_session()
            db.insert(user)

        (
            try_of(lambda: insert(user))
                .catch(lambda err: db.rollback())
                .and_finally(lambda: db.close_session())
        )
        ```
        """
        f()
        return self

    @abstractmethod
    def to_either(self) -> Either[Exception, T]:
        """
        * Returns a `Right` if it's a `Success` instance
        * Returns a `Left` if it's a `Failure` instance
        """
        raise NotImplementedError


@dataclass(frozen=True)
class Failure(Try[Any]):
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
