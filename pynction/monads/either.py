import abc
from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, TypeVar, cast

from typing_extensions import ParamSpec

L = TypeVar("L", covariant=True)
L1 = TypeVar("L1")
R = TypeVar("R", covariant=True)
R1 = TypeVar("R1")


class Either(abc.ABC, Generic[L, R]):
    @staticmethod
    def right(value: R) -> "Either[Any, R]":  # type: ignore
        return Right(value)

    @staticmethod
    def left(value: L) -> "Either[L, Any]":  # type: ignore
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
        self, predicate: Callable[[R], bool], leftValue: L  # type: ignore
    ) -> "Either[L, R]":
        raise NotImplementedError

    @abc.abstractmethod
    def get_or_else_get(self, f: Callable[[L], R]) -> R:
        raise NotImplementedError


@dataclass(frozen=True)
class Right(Either[Any, R]):
    _value: R

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
        self, satisfyCondition: Callable[[R], bool], leftValue: L  # type: ignore
    ) -> Either[L, R]:
        if satisfyCondition(self._value):
            return self
        else:
            return Left(leftValue)

    def get_or_else_get(self, _: Callable[[L], R]) -> R:
        return self._value


@dataclass(frozen=True)
class Left(Either[L, Any]):
    _value: L

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

    def filter_or_else(self, _: Callable[[R], bool], _1: L) -> Either[L, R]:  # type: ignore
        return self

    def get_or_else_get(self, f: Callable[[L], R]) -> R:
        return f(self._value)


DoEither = Generator[Either[L, R], R, R1]
P = ParamSpec("P")
"""
DoEither[L, R, R1]

This type must be used with the `@do_either` decorator.
This type just reflects the either value that is processed by the decorator,
as long as executing a "map" on the R value.
So the L and R represents the either value that the do_either receives
and R1 is the value that is returned by the function.

Example usage:
1. The `@do_either` receives an Either of type `Either[str, User]` and then returns an `Either[str, None]`

```
@do_either
def example1(id: int) -> DoEither[str, User, None]:
    user = yield find_user(id).to_either("USER_NOT_FOUND")
    user = yield execute_validation(user)
    yield execute_use_case(user)
    return None
```
"""


def do(generator: Callable[P, DoEither[L, R, R1]]) -> Callable[P, Either[L, R1]]:
    """
    `@do_either` is a decorator that enables the decoratee function to support `do` notation
    like Haskell.

    To enable this functionality you must `yield` your either value so that the decorator function
    can have control over your flow.

    Example usage:
    1. The `@do_either` receives an Either of type `Either[str, User]` and then returns an `Either[str, None]`

        1.1 If the `@do_either` receives a `left` then the flow is cut exactly in that point
            returning a Left[str] in this case

        1.2 If the `@do_either` receives a `right` the decorator just return the value
            inside of it so then your function can use it to perform anything on it
    ```
    @do_either
    def example1(id: int) -> DoEither[str, User, None]:
        user = yield find_user(id).to_either("USER_NOT_FOUND")
        user = yield execute_validation(user)
        yield execute_use_case(user)
        return None
    ```
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Either[L, R1]:
        gen = generator(*args, **kwargs)
        either_monad = next(gen)
        while True:
            try:
                if type(either_monad) == Left:
                    return either_monad
                either_monad = gen.send(cast(Right, either_monad)._value)
            except StopIteration as e:
                return Right(e.value)

    return wrapper
