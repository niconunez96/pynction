from typing import Callable, Generic, Iterable, Iterator, List, Set, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class StreamIter(Iterator[T]):
    def __init__(self, elems: Iterator[T]):
        self.elems = elems

    def __next__(self) -> T:
        return next(self.elems)


class Stream(Iterable[T], Generic[T]):
    _elems: Iterator[T]

    def __init__(
        self,
        elems: Iterable[T],
    ):
        self._elems = iter(elems)

    def map(self, f: Callable[[T], S]) -> "Stream[S]":
        return Stream(map(f, self._elems))

    def filter(self, satisfy_condition: Callable[[T], bool]) -> "Stream[T]":
        return Stream(filter(satisfy_condition, self._elems))

    def flat_map(self, f: Callable[[T], Iterable[S]]) -> "Stream[S]":
        def all_elems() -> Iterable[S]:
            for elem in self._elems:
                for new_elems in f(elem):
                    yield new_elems

        return Stream(all_elems())

    def take_while(self, satisfy_condition: Callable[[T], bool]) -> "Stream[T]":
        def take() -> Iterable[T]:
            for elem in self._elems:
                if not satisfy_condition(elem):
                    return
                yield elem

        return Stream(take())

    def __iter__(self) -> Iterator[T]:
        return StreamIter(self._elems)

    def to_list(self) -> List[T]:
        return list(self._elems)

    def to_set(self) -> Set[T]:
        return set(self._elems)


def stream(*args: T) -> Stream[T]:
    return Stream(args)


def stream_of(elems: Iterable[T]) -> Stream[T]:
    return Stream(elems)
