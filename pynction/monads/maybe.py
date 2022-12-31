import functools
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, NoReturn, Optional, TypeVar, cast

from typing_extensions import ParamSpec

from pynction.monads.either import Either, Left, Right

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)
L = TypeVar("L")


class Maybe(ABC, Generic[T]):
    """
    Maybe monad is and abstraction over a result that could contain a value
    or not. This is specially useful to avoid any errors around `None` providing
    a useful and expressive API.

    [Maybe in Haskell](http://learnyouahaskell.com/a-fistful-of-monads#getting-our-feet-wet-with-maybe)
    """

    @staticmethod
    def of(value: Optional[T]) -> "Maybe[T]":
        """
        Returns `Nothing` instance if `value` is None, for any other case
        it returns a `Just` instance with the value provided.
        """
        return Nothing.get_instance() if not value else Just(value)

    @staticmethod
    def nothing() -> "Nothing":
        """
        Factory method for `Nothing`.
        """
        return Nothing.get_instance()

    @staticmethod
    def just(value: T) -> "Just[T]":  # type: ignore
        """
        Factory method for `Just`.
        """
        return Just(value)

    @abstractproperty
    def is_empty(self) -> bool:
        """
        * Returns `True` if it's a `Nothing` instance
        * Returns `False` it it's a `Just` instance
        """
        raise NotImplementedError

    @abstractmethod
    def map(self, f: Callable[[T], V]) -> "Maybe[V]":
        """
        For `Just` instances, this method applies the `f` function over the value
        and
        * Returns `Nothing` if the result of the operation is None, else
        * Returns the result wrapped in a `Just` instance.

        For `Nothing` instances the `f` function is ignored.

        Example:
        ```
        just(1).map(lambda a: a + 1)  # Returns a Just(2)
        nothing.map(lambda a: a + 1)  # Returns Nothing
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def filter(self, satisfy_condition: Callable[[T], bool]) -> "Maybe[T]":
        """
        Returns Just(value) if this is a Just and the value satisfies the given predicate.

        Example:
        ```
        just(1).filter(lambda a: a == 1)  # Returns a Just(2)
        just(1).filter(lambda a: a > 1)  # Returns Nothing
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, f: Callable[[T], "Maybe[V]"]) -> "Maybe[V]":
        """
        For `Just` instances, this method applies the `f` function over the value.
        The difference with map is that the `f` function returns another `Maybe[V]` instead of plain `V`.

        For `Nothing` instances the `f` function is ignored.

        Example:
        ```
        just(1).flat_map(lambda a: Just(a + 1))  # Returns a Just(2)
        nothing.flat_map(lambda a: Just(a + 1))  # Returns Nothing
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: T) -> T:  # type: ignore
        """
        * Returns the value if it's a `Just` instance.
        * Returns `default` if the instance is `Nothing`.
        """
        raise NotImplementedError

    @abstractmethod
    def get_or_raise(self, error: Exception) -> T:
        """
        * Returns the value if it's a `Just` instance.
        * Raise `error` if the instance is `Nothing`.
        """
        raise NotImplementedError

    @abstractmethod
    def to_either(self, error: L) -> Either[L, T]:
        """
        * Returns `Left` with value `error` if it's a `Nothing` instance.
        * Returns `Right` with the same value of `Just` instance.

        Example
        ```
        just(1).to_either("ERROR")  # returns a Right(1)
        nothing.to_either("ERROR")  # returns a Left("ERROR")
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def on_empty(self, f: Callable[[], None]) -> None:
        """
        Runs `f` when self instance is Nothing

        Example
        ```
        just(1).on_empty(lambda: print("Hello"))  # Doesn't print
        nothing.on_empty(lambda: print("Hello"))  # Prints "Hello"
        ```
        """
        raise NotImplementedError

    @abstractmethod
    def on_just(self, f: Callable[[], None]) -> None:
        """
        Runs `f` when self instance is a Just

        Example
        ```
        just(1).on_empty(lambda: print("Hello"))  # Prints "Hello"
        nothing.on_empty(lambda: print("Hello"))  # Doesn't print
        ```
        """
        raise NotImplementedError

    def run(
        self,
        on_just: Callable[[], None] = None,
        on_empty: Callable[[], None] = None,
    ) -> None:
        """
        Runs `on_just` when self instance is a Just
        Runs `on_empty` when self instance is Nothing

        Example
        ```
        just(1).run(
            on_just=lambda: print("Hello"),
            on_empty=lambda: print("Empty"),
        )  # Prints "Hello"
        nothing.run(
            on_just=lambda: print("Hello"),
            on_empty=lambda: print("Empty"),
        )  # Prints "Empty"
        ```
        """
        if on_empty:
            self.on_empty(on_empty)
        if on_just:
            self.on_just(on_just)


@dataclass
class Nothing(Maybe[Any]):
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

    def filter(self, _: Callable[[Any], bool]) -> Maybe[Any]:
        return self

    def flat_map(self, _: Callable[[Any], Maybe[Any]]) -> Maybe[Any]:
        return self

    def get_or_else(self, default: T) -> T:  # type: ignore
        return default

    def get_or_raise(self, error: Exception) -> NoReturn:
        raise error

    def to_either(self, error: L) -> Either[L, Any]:
        return Left(error)

    def on_empty(self, f: Callable[[], None]) -> None:
        f()

    def on_just(self, _: Callable[[], None]) -> None:
        return


@dataclass(frozen=True)
class Just(Maybe[T]):
    _value: T

    def __str__(self) -> str:
        return f"Just[{self._value}]"

    @property
    def is_empty(self) -> bool:
        return False

    def map(self, f: Callable[[T], Optional[V]]) -> Maybe[V]:
        result = f(self._value)
        if not result:
            return Nothing.get_instance()
        return Just(result)

    def filter(self, satisfy_condition: Callable[[T], bool]) -> Maybe[T]:
        if satisfy_condition(self._value):
            return self
        return Nothing.get_instance()

    def flat_map(self, f: Callable[[T], Maybe[V]]) -> Maybe[V]:
        return f(self._value)

    def get_or_else(self, _: Any) -> T:
        return self._value

    def get_or_raise(self, _: Exception) -> T:
        return self._value

    def to_either(self, _: L) -> Either[L, T]:
        return Right(self._value)

    def on_empty(self, f: Callable[[], None]) -> None:
        return

    def on_just(self, f: Callable[[], None]) -> None:
        f()


DoMaybe = Generator[Maybe[T], T, V]
"""
`DoMaybe[T, V]`

This type must be used with the `@do_maybe` decorator.
This type just reflects the maybe value that is processed by the decorator.
So the `T` represents the maybe value that the do_maybe receives
and `V` is the value that is returned by the function.

Example usage:
1. The `@do_maybe` receives an Maybe of type `Maybe[User]` and then returns a `Maybe[int]`

```
@do_maybe
def example1(id: int) -> DoMaybe[str, int]:
    user = yield find_user(id)
    user = yield execute_validation(user)
    return user.age
```
"""
DoMaybeN = DoMaybe[Any, V]
"""
`DoMaybeN[R1]`

This type should be used when the function that has the `do_maybe` decorator provides
more than one type for `T`.
For this type you only need to provide the value that will result after executing the function (`V`).

In order to be able to infer the different types that your function provides
you need to use a special syntax. This syntax is the conjunction of `yield from` + `_m` helper.

Example:

```
@do_maybe
def example1(id: int) -> DoMaybeN[User]:
    name = yield from _m(obtain_name())  # mypy will infer "name" is str
    age = yield from _m(obtain_age())  # mypy will infer that "age" is int
    return User(name, age)
```
"""


def _(obj: Maybe[T]) -> DoMaybeN[T]:
    """
    This helper should be used along with `DoMaybeN` type. This helper
    is a workaround to allow dynamic typing in a do notation context.
    It should be used with `yield from`.

    Example:
    ```
    @do_maybe
    def example1(id: int) -> DoMaybeN[User]:
        name = yield from _e(obtain_name())  # mypy will infer "name" is str
        age = yield from _e(obtain_age()))  # mypy will infer that "age" is int
        return User(name, age)
    ```
    """
    a = yield obj
    return a


P = ParamSpec("P")


def do(generator: Callable[P, DoMaybe[T, V]]) -> Callable[P, Maybe[V]]:
    """
    `@do_maybe` is a decorator that enables the decorated function to support `do` notation
    like Haskell. [Do notation in Haskell](http://learnyouahaskell.com/a-fistful-of-monads#do-notation)

    To enable this functionality you must `yield` your either value so that the decorator function
    can have control over your flow.

    Example usage:
    1. The `@do_maybe` receives an Maybe of type `Maybe[User]` and then returns an `Maybe[str]`

        1.1 If the `@do_maybe` receives a `nothing` then the flow is cut exactly in that point
            returning a `Nothing` instance.

        1.2 If the `@do_maybe` receives a `just` the decorator will return the value
            inside of it so then your function can use it to perform anything on it.
    ```
    @do_maybe
    def example1(id: int) -> DoMaybe[User, str]:
        user = yield find_user(id)
        return user.name
    ```

    Example with dynamic typing:
    ```
    @do_maybe
    def example1(id: int) -> DoMaybeN[str]:
        user = yield from _m(find_user(id))  # mypy will infer that return type is User
        return user.name
    ```
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Maybe[V]:
        gen = generator(*args, **kwargs)
        maybe_monad = next(gen)
        while True:
            try:
                if isinstance(maybe_monad, Nothing):
                    return Nothing.get_instance()
                maybe_monad = gen.send(cast(Just[T], maybe_monad)._value)
            except StopIteration as e:
                return Just(e.value)

    functools.update_wrapper(wrapper, generator)
    return wrapper
