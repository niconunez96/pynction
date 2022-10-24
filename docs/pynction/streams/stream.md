Module pynction.streams.stream
==============================

Functions
---------


`stream(*args: ~T) ‑> pynction.streams.stream.Stream[~T]`
:   Factory method for `Stream` class.
    This method takes N number of arguments and creates
    a `Stream` of them.

    Example
    ```
    stream(1, 2, 3, 4)  # Returns Stream[int]
    ```


`stream_of(elems: Iterable[~T]) ‑> pynction.streams.stream.Stream[~T]`
:   Factory method for `Stream` class.
    This method takes an iterable and creates a `Stream` of it.

    Example
    ```
    stream_of([1, 2, 3, 4])  # Returns Stream[int]
    stream_of({"1", "2", "3", "4"})  # Returns Stream[str]
    stream_of(range(1, 20))  # Returns Stream[int]
    ```

Classes
-------

`Stream(elems: Iterable[~T])`
:   Stream class provides a set of functionality to operate over it
    in a functional way.
    It operates in a "lazy" way to avoid any memory overhead.

    ### Ancestors (in MRO)

    * collections.abc.Iterable
    * typing.Generic

    ### Methods

    `filter(self, satisfy_condition: Callable[[~T], bool]) ‑> pynction.streams.stream.Stream[~T]`
    :   Applies `satisfy_condition` over each value and returns a new
        `Stream` with values that have satisfied the condition.

        Example
        ```
        stream(1, 2, 3, 4, 5, 6, 7)
            .filter(lambda a: a < 5)
            .to_list()  # Returns [1, 2, 3, 4]
        ```

    `flat_map(self, f: Callable[[~T], Iterable[~S]]) ‑> pynction.streams.stream.Stream[~S]`
    :   Applies the `f` function on each value
        and then flattens the global result into a single `Stream` of elements.

        Example
        ```
        (
            stream(1, 2, 3, 4)
            .flat_map(lambda a: [a, a])
            .to_list()
        )  # Returns [1, 1, 2, 2, 3, 3, 4, 4]
        ```

    `map(self, f: Callable[[~T], ~S]) ‑> pynction.streams.stream.Stream[~S]`
    :   If it is a `Stream` with one element or more,
        this method applies the `f` function on each value and returns the result `Stream`.

        If the `Stream` is empty the `f` function is ignored.

        Example:
        ```
        stream_of(1, 2).map(str)  # Returns `Stream[str]`
        ```

    `take_while(self, satisfy_condition: Callable[[~T], bool]) ‑> pynction.streams.stream.Stream[~T]`
    :   Takes the first N elements of `Stream` while each element evaluate `satisfy_condition` as True

    `to_list(self) ‑> List[~T]`
    :

    `to_set(self) ‑> Set[~T]`
    :

`StreamIter(elems: Iterator[~T])`
:   `StreamIter` makes `Stream` iterable using for loops or
    for comprehension syntax.

    ### Ancestors (in MRO)

    * collections.abc.Iterator
    * collections.abc.Iterable
    * typing.Generic
