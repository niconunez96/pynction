from typing import Callable, Generic, Iterable, List, Set, Tuple, TypeVar

T = TypeVar("T")
S = TypeVar("S")
Predicate = Callable[..., bool]


class Stream(Generic[T]):
    _elems: Iterable[T]

    def __init__(self, *args: T):
        self._elems = iter(args)

    @staticmethod
    def of(elems: Iterable[T]) -> "Stream[T]":
        return Stream(*elems)

    def map(self, f: Callable[[T], S]) -> "Stream[S]":
        return Stream.of((f(elem) for elem in self._elems))

    def filter(self, satisfyCondition: Predicate) -> "Stream[T]":
        return Stream.of((elem for elem in self._elems if satisfyCondition(elem)))

    def flat_map(self, f: Callable[[T], Iterable[S]]) -> "Stream[S]":
        def all_elems():
            for elem in self._elems:
                for new_elems in f(elem):
                    yield new_elems

        return Stream.of(all_elems())

    def take_while(self, satisfyCondition: Predicate) -> "Stream[T]":
        def take():
            for elem in self._elems:
                if not satisfyCondition(elem):
                    return
                yield elem

        return Stream(take())

    @property
    def to_list(self) -> List[T]:
        return list(self._elems)

    @property
    def to_set(self) -> Set[T]:
        return set(self._elems)
