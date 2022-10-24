Module pynction.functors.function
=================================

Classes
-------

`Function(f: Callable[[~T], ~R])`
:   Class that represents a function with a single argument.

    ### Ancestors (in MRO)

    * pynction.functors.Functor
    * typing.Generic
    * typing_extensions.Protocol

    ### Static methods

    `decorator(decorated: Callable[[~T], ~R]) ‑> pynction.functors.function.Function[~T, ~R]`
    :   Decorator that transforms your function with a single argument
        to a `Function` instance

    ### Methods

    `map(self, f: Union[Callable[[~R], ~R2], ForwardRef('Function[R, R2]')]) ‑> pynction.functors.function.Function[~T, ~R2]`
    :   This method implements the `Functor` interface which in this case
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

`Function2(f: Callable[[~T, ~T2], ~R])`
:   Class that represents a function with 2 arguments.

    ### Ancestors (in MRO)

    * pynction.functors.Functor
    * typing.Generic
    * typing_extensions.Protocol

    ### Static methods

    `decorator(decorated: Callable[[~T, ~T2], ~R]) ‑> pynction.functors.function.Function2[~T, ~T2, ~R]`
    :   Decorator that transforms your function with a single argument
        to a `Function2` instance

    ### Instance variables

    `curried: pynction.functors.function.Function[~T, pynction.functors.function.Function[~T2, ~R]]`
    :   This method transform your function of 2 argument into 2 composed functions
        of one argument each one.
        Example
        ```
        f1 = Function2(lambda a, b: a + b)
        f2 = f1.curried
        f1(15, 15) == f2(15)(15)
        ```

    ### Methods

    `map(self, f: Union[Callable[[~R], ~R2], ForwardRef('Function[R, R2]')]) ‑> pynction.functors.function.Function2[~T, ~T2, ~R2]`
    :   This method implements the `Functor` interface which in this case
        is used to compose functions.

        Math syntax
        ```
        f1(x, y) => z
        f2(z) => v
        f2(f1(32, 32)) => v
        ```

        Pynction syntax
        ```
        f1 = Function2(lambda a, b: a + b)
        f2 = lambda a: a + 10
        f3 = f1.map(f2)
        f3(2, 2) # will return => 14
        ```

`Function3(f: Callable[[~T, ~T2, ~T3], ~R])`
:   Class that represents a function with 3 arguments.

    ### Ancestors (in MRO)

    * pynction.functors.Functor
    * typing.Generic
    * typing_extensions.Protocol

    ### Static methods

    `decorator(decorated: Callable[[~T, ~T2, ~T3], ~R]) ‑> pynction.functors.function.Function3[~T, ~T2, ~T3, ~R]`
    :   Decorator that transforms your function with a single argument
        to a `Function3` instance

    ### Instance variables

    `curried: pynction.functors.function.Function[~T, pynction.functors.function.Function[~T2, pynction.functors.function.Function[~T3, ~R]]]`
    :   This method transform your function of 3 argument into 3 composed functions
        of one argument each one.
        Example
        ```
        f1 = Function3(lambda a, b, c: a + b + c)
        f2 = f1.curried
        f1(15, 15, 10) == f2(15)(15)(10)
        ```

    ### Methods

    `map(self, f: Union[Callable[[~R], ~R2], ForwardRef('Function[R, R2]')]) ‑> pynction.functors.function.Function3[~T, ~T2, ~T3, ~R2]`
    :   This method implements the `Functor` interface which in this case
        is used to compose functions.

        Math syntax
        ```
        f1(x, y, z) => v
        f2(v) => w
        f2(f1(2, 2, 10)) => p
        ```

        Pynction syntax
        ```
        f1 = Function3(lambda a, b, c: a + b + c)
        f2 = lambda a: a + 10
        f3 = f1.map(f2)
        f3(2, 2, 10) # will return => 24
        ```

`Function4(f: Callable[[~T, ~T2, ~T3, ~T4], ~R])`
:   Class that represents a function with 4 arguments.

    ### Ancestors (in MRO)

    * pynction.functors.Functor
    * typing.Generic
    * typing_extensions.Protocol

    ### Static methods

    `decorator(decorated: Callable[[~T, ~T2, ~T3, ~T4], ~R]) ‑> pynction.functors.function.Function4[~T, ~T2, ~T3, ~T4, ~R]`
    :   Decorator that transforms your function with a single argument
        to a `Function4` instance

    ### Instance variables

    `curried: pynction.functors.function.Function[~T, pynction.functors.function.Function[~T2, pynction.functors.function.Function[~T3, pynction.functors.function.Function[~T4, ~R]]]]`
    :   This method transform your function of 3 argument into 3 composed functions
        of one argument each one.
        Example
        ```
        f1 = Function3(lambda a, b, c, d: a + b + c + d)
        f2 = f1.curried
        f1(15, 15, 10, 2) == f2(15)(15)(10)(2)
        ```

    ### Methods

    `map(self, f: Union[Callable[[~R], ~R2], ForwardRef('Function[R, R2]')]) ‑> pynction.functors.function.Function4[~T, ~T2, ~T3, ~T4, ~R2]`
    :   This method implements the `Functor` interface which in this case
        is used to compose functions.

        Math syntax
        ```
        f1(x, y, z, v) => w
        f2(w) => p
        f2(f1(2, 2, 10, 11)) => t
        ```

        Pynction syntax
        ```
        f1 = Function4(lambda a, b, c, d: a + b + c + d)
        f2 = lambda a: a + 10
        f3 = f1.map(f2)
        f3(2, 2, 10, 11) # will return => 35
        ```

`Provider(f: Callable[[], ~R])`
:   Class that represents a function without arguments.

    ### Ancestors (in MRO)

    * pynction.functors.Functor
    * typing.Generic
    * typing_extensions.Protocol

    ### Static methods

    `decorator(decorated: Callable[[], ~R]) ‑> pynction.functors.function.Provider[~R]`
    :   Decorator that transforms your function without arguments
        to a `Provider` instance

    ### Methods

    `map(self, f: Union[Callable[[~R], ~R2], ForwardRef('Function[R, R2]')]) ‑> pynction.functors.function.Provider[~R2]`
    :   This method implements the `Functor` interface which in this case
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
