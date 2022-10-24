from typing import Callable, Iterable, Iterator, List, Set, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class StreamIter(Iterator[T]):
    """
    `StreamIter` makes `Stream` iterable using for loops or
    for comprehension syntax.
    """

    def __init__(self, elems: Iterator[T]):
        self.elems = elems

    def __next__(self) -> T:
        return next(self.elems)


class Stream(Iterable[T]):
    """
    Stream class provides a set of functionality to operate over it
    in a functional way.
    It operates in a "lazy" way to avoid any memory overhead.
    """

    _elems: Iterator[T]

    def __init__(
        self,
        elems: Iterable[T],
    ):
        self._elems = iter(elems)

    def map(self, f: Callable[[T], S]) -> "Stream[S]":
        """
        If it is a `Stream` with one element or more,
        this method applies the `f` function on each value and returns the result `Stream`.

        If the `Stream` is empty the `f` function is ignored.

        Example:
        ```
        stream_of(1, 2).map(str)  # Returns `Stream[str]`
        ```
        """
        return Stream(map(f, self._elems))

    def filter(self, satisfy_condition: Callable[[T], bool]) -> "Stream[T]":
        """
        Applies `satisfy_condition` over each value and returns a new
        `Stream` with values that have satisfied the condition.

        Example
        ```
        stream(1, 2, 3, 4, 5, 6, 7)
            .filter(lambda a: a < 5)
            .to_list()  # Returns [1, 2, 3, 4]
        ```
        """
        return Stream(filter(satisfy_condition, self._elems))

    def flat_map(self, f: Callable[[T], Iterable[S]]) -> "Stream[S]":
        """
        Applies the `f` function on each value
        and then flattens the global result into a single `Stream` of elements.

        Example
        ```
        (
            stream(1, 2, 3, 4)
            .flat_map(lambda a: [a, a])
            .to_list()
        )  # Returns [1, 1, 2, 2, 3, 3, 4, 4]
        ```
        """

        def all_elems() -> Iterable[S]:
            for elem in self._elems:
                for new_elems in f(elem):
                    yield new_elems

        return Stream(all_elems())

    def take_while(self, satisfy_condition: Callable[[T], bool]) -> "Stream[T]":
        """
        Takes the first N elements of `Stream` while each element evaluate `satisfy_condition` as True
        """

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
    """
    Factory method for `Stream` class.
    This method takes N number of arguments and creates
    a `Stream` of them.

    Example
    ```
    stream(1, 2, 3, 4)  # Returns Stream[int]
    ```
    """
    return Stream(args)


def stream_of(elems: Iterable[T]) -> Stream[T]:
    """
    Factory method for `Stream` class.
    This method takes an iterable and creates a `Stream` of it.

    Example
    ```
    stream_of([1, 2, 3, 4])  # Returns Stream[int]
    stream_of({"1", "2", "3", "4"})  # Returns Stream[str]
    stream_of(range(1, 20))  # Returns Stream[int]
    ```
    """
    return Stream(elems)
