from types import GeneratorType
from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    Set,
    TypeVar,
)

T = TypeVar("T")
S = TypeVar("S")


class StreamIter(Iterator[T]):
    def __init__(self, elems: Iterator[T]):
        self.elems = elems

    def __next__(self):
        return next(self.elems)


class Stream(Iterable[T], Generic[T]):
    _elems: Iterator[T]

    def __init__(
        self,
        *elems: T,
    ):
        if len(elems) == 1 and type(elems[0]) in (
            list,
            set,
            tuple,
            map,
            filter,
            GeneratorType,
            range,
        ):
            self._elems = iter(elems[0])  # type: ignore
        else:
            self._elems = iter(elems)

    @staticmethod
    def of(elems: Iterable[T]) -> "Stream[T]":
        return Stream(elems)  # type: ignore

    def map(self, f: Callable[[T], S]) -> "Stream[S]":
        return Stream.of(map(f, self._elems))

    def filter(self, satisfy_condition: Callable[[T], bool]) -> "Stream[T]":
        return Stream.of(filter(satisfy_condition, self._elems))

    def flat_map(self, f: Callable[[T], Iterable[S]]) -> "Stream[S]":
        def all_elems():
            for elem in self._elems:
                for new_elems in f(elem):
                    yield new_elems

        return Stream.of(all_elems())

    def take_while(self, satisfy_condition: Callable[[T], bool]) -> "Stream[T]":
        def take():
            for elem in self._elems:
                if not satisfy_condition(elem):
                    return
                yield elem

        return Stream.of(take())

    def __iter__(self) -> Iterator[T]:
        return StreamIter(self._elems)

    @property
    def to_list(self) -> List[T]:
        return list(self._elems)

    @property
    def to_set(self) -> Set[T]:
        return set(self._elems)
