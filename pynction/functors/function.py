import functools
from typing import Callable, Generic, TypeVar, Union

from pynction.functors import Functor

T = TypeVar("T")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
R = TypeVar("R")
R2 = TypeVar("R2")


class Provider(Functor[R]):
    """
    Class that represents a function without arguments.
    """

    def __init__(self, f: Callable[[], R]) -> None:
        self._f = f

    def __call__(self) -> R:
        """
        This method makes any instance of this class `callable`
        so you can do the following
        ```
        f1 = Provider(lambda: 32)
        f1()  # will return => 32
        ```
        """
        return self._f()

    def map(self, f: Union[Callable[[R], R2], "Function[R, R2]"]) -> "Provider[R2]":
        """
        This method implements the `Functor` interface which in this case
        is used to compose functions.

        Math syntax
        ```
        f1() => y
        f2(y) => z
        f2(f1()) => z
        ```

        Pynction syntax
        ```
        f1 = Provider(lambda: 32)
        f2 = lambda a: a + 10
        f3 = f1.map(f2)
        f3() # will return => 42
        ```
        """
        return Provider(lambda: f(self._f()))

    def __or__(self, f: Union[Callable[[R], R2], "Function[R, R2]"]) -> "Provider[R2]":
        """
        Syntax sugar for `map` method so you can do the following
        ```
        f1 = Provider(lambda: 32)
        f2 = lambda a: a + 10
        f3 = f1 | f2
        f3() # will return => 42
        ```
        """
        return self.map(f)

    @staticmethod
    def decorator(decorated: Callable[[], R]) -> "Provider[R]":
        """
        Decorator that transform your function without arguments
        to a `Provider` instance
        """

        def decorator() -> R:
            return decorated()

        functools.update_wrapper(decorator, decorated)
        return Provider(decorator)


class Function(Functor[R], Generic[T, R]):
    """
    Class that represents a function with a single argument.
    """

    def __init__(self, f: Callable[[T], R]) -> None:
        self._f = f

    def __call__(self, arg: T) -> R:
        """
        This method makes any instance of this class `callable`
        so you can do the following
        ```
        f1 = Function(lambda a: a + 32)
        f1(2)  # will return => 34
        ```
        """
        return self._f(arg)

    def map(self, f: Union[Callable[[R], R2], "Function[R, R2]"]) -> "Function[T, R2]":
        """
        This method implements the `Functor` interface which in this case
        is used to compose functions.

        Math syntax
        ```
        f1(x) => y
        f2(y) => z
        f2(f1(32)) => z
        ```

        Pynction syntax
        ```
        f1 = Function(lambda a: a + 32)
        f2 = lambda a: a + 10
        f3 = f1.map(f2)
        f3(2) # will return => 44
        ```
        """
        return Function(lambda x: f(self._f(x)))

    def __or__(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function[T, R2]":
        """
        Syntax sugar for `map` method so you can do the following
        ```
        f1 = Function(lambda a: a + 32)
        f2 = lambda a: a + 10
        f3 = f1 | f2
        f3(2) # will return => 44
        ```
        """
        return self.map(f)

    @staticmethod
    def decorator(decorated: Callable[[T], R]) -> "Function[T, R]":
        """
        Decorator that transform your function with a single argument
        to a `Function` instance
        """

        def decorator(arg: T) -> R:
            return decorated(arg)

        functools.update_wrapper(decorator, decorated)
        return Function(decorator)


class Function2(Generic[T, T2, R]):
    def __init__(self, f: Callable[[T, T2], R]) -> None:
        self._f = f

    def __call__(self, arg: T, arg2: T2) -> R:
        return self._f(arg, arg2)

    def map(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function2[T, T2, R2]":
        return Function2(lambda x, y: f(self._f(x, y)))

    def __or__(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function2[T, T2, R2]":
        return self.map(f)

    @property
    def curried(self) -> Function[T, Function[T2, R]]:
        return Function(lambda x: Function(lambda y: self._f(x, y)))

    @staticmethod
    def decorator(decoratee: Callable[[T, T2], R]) -> "Function2[T, T2, R]":
        def decorator(arg: T, arg2: T2) -> R:
            return decoratee(arg, arg2)

        return Function2(decorator)


class Function3(Generic[T, T2, T3, R]):
    def __init__(self, f: Callable[[T, T2, T3], R]) -> None:
        self._f = f

    def __call__(self, arg: T, arg2: T2, arg3: T3) -> R:
        return self._f(arg, arg2, arg3)

    def map(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function3[T, T2, T3, R2]":
        return Function3(lambda x, y, z: f(self._f(x, y, z)))

    def __or__(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function3[T, T2, T3, R2]":
        return self.map(f)

    @property
    def curried(self) -> Function[T, Function[T2, Function[T3, R]]]:
        return Function(
            lambda x: Function(lambda y: Function(lambda z: self._f(x, y, z)))
        )

    @staticmethod
    def decorator(decoratee: Callable[[T, T2, T3], R]) -> "Function3[T, T2, T3, R]":
        def decorator(arg: T, arg2: T2, arg3: T3) -> R:
            return decoratee(arg, arg2, arg3)

        return Function3(decorator)


class Function4(Generic[T, T2, T3, T4, R]):
    def __init__(self, f: Callable[[T, T2, T3, T4], R]) -> None:
        self._f = f

    def __call__(self, arg: T, arg2: T2, arg3: T3, arg4: T4) -> R:
        return self._f(arg, arg2, arg3, arg4)

    def map(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function4[T, T2, T3, T4, R2]":
        return Function4(lambda x, y, z, q: f(self._f(x, y, z, q)))

    def __or__(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function4[T, T2, T3, T4, R2]":
        return self.map(f)

    @property
    def curried(self) -> Function[T, Function[T2, Function[T3, Function[T4, R]]]]:
        return Function(
            lambda x: Function(
                lambda y: Function(lambda z: Function(lambda q: self._f(x, y, z, q)))
            )
        )

    @staticmethod
    def decorator(
        decoratee: Callable[[T, T2, T3, T4], R]
    ) -> "Function4[T, T2, T3, T4, R]":
        def decorator(arg: T, arg2: T2, arg3: T3, arg4: T4) -> R:
            return decoratee(arg, arg2, arg3, arg4)

        return Function4(decorator)
