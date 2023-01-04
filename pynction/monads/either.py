import abc
import functools
from dataclasses import dataclass
from inspect import signature
from typing import Any, Callable, Generator, Generic, TypeVar, Union, cast

from typing_extensions import ParamSpec

L = TypeVar("L", covariant=True)
L1 = TypeVar("L1")
R = TypeVar("R", covariant=True)
R1 = TypeVar("R1")


class Either(abc.ABC, Generic[L, R]):
    """
    Either monad is an abstraction of a result that could be 2 things.
    It's super useful for error handling, by "standard" the left value
    is used for errors and the right value is used for successful results.
    [Either in Haskell](http://learnyouahaskell.com/for-a-few-monads-more#error)
    """

    @staticmethod
    def right(value: R) -> "Either[Any, R]":  # type: ignore
        """
        Creates a `Right` instance with the given type
        """
        return Right(value)

    @staticmethod
    def left(value: L) -> "Either[L, Any]":  # type: ignore
        """
        Creates a `Left` instance with the given type
        """
        return Left(value)

    @abc.abstractproperty
    def is_left(self) -> bool:
        """
        Checks if the current instance is a `Left` instance
        """
        raise NotImplementedError

    @abc.abstractproperty
    def is_right(self) -> bool:
        """
        Checks if the current instance is a `Right` instance
        """
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, mapper: Callable[[R], R1]) -> "Either[L, R1]":
        """
        Applies `f` over the right value. If the instance is a `Left`
        the function `f` is ignored.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def filter_or_else(
        self,
        predicate: Callable[[R], bool],
        left_value: L,  # type: ignore
    ) -> "Either[L, R]":
        """
        Evaluate the `predicate` over the right value, if the result is
        `True` the returned either is the same `Right` instance but if the
        predicate is not satisfied then the result is a `Left` instance with
        the `left_value`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_or_else_get(self, provider: Callable[[L], R]) -> R:
        """
        It returns the right value if the instance is `Right`
        but if the instance is a `Left` it applies the `f` function and return
        the result obtained by that function.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def recover(
        self,
        recovery_handler: Union[Callable[[L], R], Callable[[], R]],
    ) -> "Either[L, R]":
        """
        Calls `recovery_handler` if the projected Either is a Left, or returns this if Right.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def on_right(self, consumer: Callable[[R], None]) -> "Either[L, R]":
        """
        Calls `consumer` if the projected Either is a Right.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def on_left(self, consumer: Callable[[L], None]) -> "Either[L, R]":
        """
        Calls `consumer` if the projected Either is a Left.
        """
        raise NotImplementedError

    def run(
        self,
        on_right: Callable[[R], None] = None,
        on_left: Callable[[L], None] = None,
    ) -> None:
        """
        Runs `on_right` when self instance is a Right
        Runs `on_left` when self instance is a Left

        Example
        ```python
        right(1).run(
            on_right=lambda value: print(f"Hello {value}"),
            on_left=lambda error: print(f"Error: {error}"),
        )  # Prints "Hello 1"
        left("boom!").run(
            on_right=lambda value: print(f"Hello {value}"),
            on_left=lambda error: print(f"Error: {error}"),
        )  # Prints "Error: boom!"
        ```
        """
        if on_right:
            self.on_right(on_right)
        if on_left:
            self.on_left(on_left)


@dataclass(frozen=True)
class Right(Either[Any, R]):
    _value: R

    def __str__(self) -> str:
        return f"Right[{self._value}]"

    @property
    def is_left(self) -> bool:
        return False

    @property
    def is_right(self) -> bool:
        return True

    def map(self, mapper: Callable[[R], R1]) -> Either[L, R1]:
        return Right(mapper(self._value))

    def filter_or_else(
        self,
        satisfy_condition: Callable[[R], bool],
        left_value: L,  # type: ignore
    ) -> Either[L, R]:
        if satisfy_condition(self._value):
            return self
        else:
            return Left(left_value)

    def get_or_else_get(self, _: Callable[[L], R]) -> R:
        return self._value

    def recover(self, _: Union[Callable[[L], R], Callable[[], R]]) -> Either[L, R]:
        return self

    def on_right(self, consumer: Callable[[R], None]) -> Either[L, R]:
        consumer(self._value)
        return self

    def on_left(self, _: Callable[[L], None]) -> Either[L, R]:
        return self


@dataclass(frozen=True)
class Left(Either[L, Any]):
    _value: L

    def __str__(self) -> str:
        return f"Left[{self._value}]"

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

    def get_or_else_get(self, provider: Callable[[L], R]) -> R:
        return provider(self._value)

    def recover(
        self,
        recovery_handler: Union[Callable[[L], R], Callable[[], R]],
    ) -> Either[L, R]:
        if len(signature(recovery_handler).parameters) == 0:
            return Either.right(cast(Callable[[], R], recovery_handler)())
        return Either.right(cast(Callable[[L], R], recovery_handler)(self._value))

    def on_right(self, _: Callable[[R], None]) -> Either[L, R]:
        return self

    def on_left(self, consumer: Callable[[L], None]) -> Either[L, R]:
        consumer(self._value)
        return self


P = ParamSpec("P")
DoEither = Generator[Either[L, R], R, R1]
"""
`DoEither[L, R, R1]`

This type must be used with the `@do_either` decorator.
This type just reflects the either value that is processed by the decorator.
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


DoEitherN = DoEither[L, Any, R1]
"""
`DoEitherN[L, R1]`

This type should be used when the function that has the `do_either` decorator provides
more than one type for `R`. For this type you only need to provide the left type
that the function will return (`L`) and the right value that will result after executing the function (`R1`).

In order to be able to infer the different types that your function provides
you need to use a special syntax. This syntax is the conjunction of `yield from` + `_e` helper.

Example:

```
@do_either
def example1(id: int) -> DoEitherN[str, User]:
    name = yield from _e(obtain_name())  # mypy will infer "name" is str
    age = yield from _e(obtain_age())  # mypy will infer that "age" is int
    return User(name, age)
```
"""


def _(obj: Either[L, R]) -> DoEitherN[L, R]:
    """
    This helper should be used along with `DoEitherN` type. This helper
    is a workaround to allow dynamic typing in a do notation context.
    It should be used with `yield from`

    Example:
    ```
    @do_either
    def example1(id: int) -> DoEitherN[str, User]:
        name = yield from _e(obtain_name())  # mypy will infer "name" is str
        age = yield from _e(obtain_age())  # mypy will infer that "age" is int
        return User(name, age)
    ```
    """
    a = yield obj
    return a


def do(generator: Callable[P, DoEither[L, R, R1]]) -> Callable[P, Either[L, R1]]:
    """
    `@do_either` is a decorator that enables the decorated function to support `do` notation
    like Haskell. [Do notation in Haskell](http://learnyouahaskell.com/a-fistful-of-monads#do-notation)

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

    Example with dynamic typing
    ```
    @do_either
    def example1(id: int) -> DoEitherN[str, User]:
        name = yield from _e(obtain_name())  # mypy will infer "name" is str
        age = yield from _e(obtain_age())  # mypy will infer that "age" is int
        return User(name, age)
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

    functools.update_wrapper(wrapper, generator)
    return wrapper
