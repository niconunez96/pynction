Module pynction.monads.maybe
============================

Variables
---------


`DoMaybe`
:   `DoMaybe[T, V]`

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


`DoMaybeN`
:   `DoMaybeN[R1]`

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

Functions
---------


`do(generator: Callable[[~P], Generator[pynction.monads.maybe.Maybe[+T], +T, +V]]) ‑> Callable[[~P], pynction.monads.maybe.Maybe[+V]]`
:   `@do_maybe` is a decorator that enables the decorated function to support `do` notation
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

Classes
-------

`Just(_value: +T)`
:   Just(*args, **kwds)

    ### Ancestors (in MRO)

    * pynction.monads.maybe.Maybe
    * abc.ABC
    * typing.Generic

`Maybe(*args, **kwds)`
:   Maybe monad is and abstraction over a result that could contain a value
    or not. This is specially useful to avoid any errors around `None` providing
    a useful and expressive API.

    [Maybe in Haskell](http://learnyouahaskell.com/a-fistful-of-monads#getting-our-feet-wet-with-maybe)

    ### Ancestors (in MRO)

    * abc.ABC
    * typing.Generic

    ### Descendants

    * pynction.monads.maybe.Just
    * pynction.monads.maybe.Nothing

    ### Static methods

    `just(value: +T) ‑> pynction.monads.maybe.Just[+T]`
    :   Factory method for `Just`.

    `nothing() ‑> pynction.monads.maybe.Nothing`
    :   Factory method for `Nothing`.

    `of(value: Optional[+T]) ‑> pynction.monads.maybe.Maybe[+T]`
    :   Returns `Nothing` instance if `value` is None, for any other case
        it returns a `Just` instance with the value provided.

    ### Instance variables

    `is_empty: bool`
    :   * Returns `True` if it's a `Nothing` instance
        * Returns `False` it it's a `Just` instance

    ### Methods

    `flat_map(self, f: Callable[[+T], ForwardRef('Maybe[V]')]) ‑> pynction.monads.maybe.Maybe[+V]`
    :   If it is a `Just` instance, this method applies the `f` function over the value
        and returns the `Maybe` instance returned by `f`.
        For `Nothing` instances the `f` function is ignored.

        The difference with map is that the `f` function returns another `Maybe[V]` instead of plain `V`

        Example:
        ```
        just(1).flat_map(lambda a: Just(a + 1))  # Returns a Just(2)
        nothing.flat_map(lambda a: Just(a + 1))  # Returns Nothing
        ```

    `get_or_else(self, default: +T) ‑> +T`
    :   * Returns the value if it's a `Just` instance.
        * Returns `default` if the instance is `Nothing`.

    `get_or_raise(self, error: Exception) ‑> +T`
    :   * Returns the value if it's a `Just` instance.
        * Raise `error` if the instance is `Nothing`.

    `map(self, f: Callable[[+T], +V]) ‑> pynction.monads.maybe.Maybe[+V]`
    :   If it is a `Just` instance, this method applies the `f` function over the value
        and
        * Returns `Nothing` if the result of the operation is None, else
        * Returns the result wrapped in a `Just` instance.

        For `Nothing` instances the `f` function is ignored.

        Example:
        ```
        just(1).map(lambda a: a + 1)  # Returns a Just(2)
        nothing.map(lambda a: a + 1)  # Returns Nothing
        ```

    `to_either(self, error: ~L) ‑> pynction.monads.either.Either[~L, +T]`
    :   * Returns `Left` with value `error` if it's a `Nothing` instance.
        * Returns `Right` with the same value of `Just` instance.

        Example
        ```
        just(1).to_either("ERROR")  # returns a Right(1)
        nothing.to_either("ERROR")  # returns a Left("ERROR")
        ```

`Nothing()`
:   Nothing(*args, **kwds)

    ### Ancestors (in MRO)

    * pynction.monads.maybe.Maybe
    * abc.ABC
    * typing.Generic

    ### Static methods

    `get_instance() ‑> pynction.monads.maybe.Nothing`
    :
