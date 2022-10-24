Module pynction.monads.either
=============================

Variables
---------


`DoEither`
:   `DoEither[L, R, R1]`

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


`DoEitherN`
:   `DoEitherN[L, R1]`

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

Functions
---------


`do(generator: Callable[[~P], Generator[pynction.monads.either.Either[+L, +R], +R, ~R1]]) ‑> Callable[[~P], pynction.monads.either.Either[+L, ~R1]]`
:   `@do_either` is a decorator that enables the decorated function to support `do` notation
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

Classes
-------

`Either(*args, **kwds)`
:   Either monad is an abstraction of a result that could be 2 things.
    It's super useful for error handling, by "standard" the left value
    is used for errors and the right value is used for successful results.
    [Either in Haskell](http://learnyouahaskell.com/for-a-few-monads-more#error)

    ### Ancestors (in MRO)

    * abc.ABC
    * typing.Generic

    ### Descendants

    * pynction.monads.either.Left
    * pynction.monads.either.Right

    ### Static methods

    `left(value: +L) ‑> pynction.monads.either.Either[+L, typing.Any]`
    :   Creates a `Left` instance with the given type

    `right(value: +R) ‑> pynction.monads.either.Either[typing.Any, +R]`
    :   Creates a `Right` instance with the given type

    ### Instance variables

    `is_left: bool`
    :   Checks if the current instance is a `Left` instance

    `is_right: bool`
    :   Checks if the current instance is a `Right` instance

    ### Methods

    `filter_or_else(self, predicate: Callable[[+R], bool], left_value: +L) ‑> pynction.monads.either.Either[+L, +R]`
    :   Evaluate the `predicate` over the right value, if the result is
        `True` the returned either is the same `Right` instance but if the
        predicate is not satisfied then the result is a `Left` instance with
        the `left_value`

    `get_or_else_get(self, f: Callable[[+L], +R]) ‑> +R`
    :   It returns the right value if the instance is `Right`
        but if the instance is a `Left` it applies the `f` function and return
        the result obtained by that function.

    `map(self, f: Callable[[+R], ~R1]) ‑> pynction.monads.either.Either[+L, ~R1]`
    :   Applies `f` over the right value. If the instance is a `Left`
        the function `f` is ignored.

`Left(_value: +L)`
:   Left(*args, **kwds)

    ### Ancestors (in MRO)

    * pynction.monads.either.Either
    * abc.ABC
    * typing.Generic

`Right(_value: +R)`
:   Right(*args, **kwds)

    ### Ancestors (in MRO)

    * pynction.monads.either.Either
    * abc.ABC
    * typing.Generic
