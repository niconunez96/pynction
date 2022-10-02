from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
R = TypeVar("R")
R2 = TypeVar("R2")


class Provider(Generic[R]):
    def __init__(self, f: Callable[[], R]) -> None:
        self._f = f

    def __call__(self) -> R:
        return self._f()

    def map(self, f: Union[Callable[[R], R2], "Function[R, R2]"]) -> "Provider[R2]":
        return Provider(lambda: f(self._f()))

    def __or__(self, f: Union[Callable[[R], R2], "Function[R, R2]"]) -> "Provider[R2]":
        return self.map(f)

    @staticmethod
    def decorator(decoratee: Callable[[], R]) -> "Provider[R]":
        def decorator() -> R:
            return decoratee()

        return Provider(decorator)


class Function(Generic[T, R]):
    def __init__(self, f: Callable[[T], R]) -> None:
        self._f = f

    def __call__(self, arg: T) -> R:
        return self._f(arg)

    def map(self, f: Union[Callable[[R], R2], "Function[R, R2]"]) -> "Function[T, R2]":
        return Function(lambda x: f(self._f(x)))

    def __or__(
        self, f: Union[Callable[[R], R2], "Function[R, R2]"]
    ) -> "Function[T, R2]":
        return self.map(f)

    @staticmethod
    def decorator(decoratee: Callable[[T], R]) -> "Function[T, R]":
        def decorator(arg: T) -> R:
            return decoratee(arg)

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
