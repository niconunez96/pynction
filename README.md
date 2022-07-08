# Pynction 🐍

[![continuous_integration](https://github.com/niconunez96/pynction/actions/workflows/ci.yaml/badge.svg)](https://github.com/niconunez96/pynction/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/niconunez96/pynction/branch/main/graph/badge.svg?token=YI2ZOWV29E)](https://codecov.io/gh/niconunez96/pynction)

Functional based library to support haskell monads like Either, Maybe in a scala fashion style. The library also contains Try monad inspired from vavr and a Stream class which is pretty similar to scala and java stream API

Inspired in: [VΛVR](https://github.com/vavr-io/vavr)

## Why should you use it ?

Probably if you have reached this library you already know something about functional programming and Monads.
Well this library is another one that empowers your imperative code to start using functional programming concepts. This type of programming makes your code declarative as long as give you support to the most famous monads like `Maybe` and `Either`.
These monads make your interfaces explicit for error handling so paraphrasing `If it compiles, it works` this time it is `If mypy is happy, your code works`

## Basic examples

### Stream examples

```python
from pynction import stream_of, stream


foo = (
    stream_of([1, 2, 3, 4])
    .map(lambda a: a + 1)
    .filter(lambda n: n % 2 == 0)
    .flat_map(lambda n: [n, n * 2])
    .to_list
)

# foo => [2, 4, 4, 8]

bar = (
    stream("example", "e", "something")
    .take_while(lambda s: s.startswith("e"))
    .to_list
)

# bar => ["example", "e"]
```

### Maybe examples

```python
from pynction import maybe, nothing

def divide_10_by(n: int) -> Maybe[int]:
    if n == 0:
        return nothing
    return maybe(10 / n)

result = divide_10_by(2).get_or_else_get(-1)
# result => 5
result = divide_10_by(0).get_or_else_get(-1)
# result => -1
```

### Try examples

```python
from pynction import try_of


def add_10(n: int) -> int:
    if n > 10:
        raise Exception("n must be less than 10")
    return n + 10

try_example_1 = try_of(lambda: add_10(11)).map(lambda a: a + 1)
try_example_1.on(
    on_success=lambda a: print(f"Result: {a}"),
    on_failure=lambda e: print(f"Error: {e}"),
)
# ==> Will print "Error: n must be less than 10"

try_example_2 = try_of(lambda: add_10(9)).map(lambda a: a + 1)
try_example_2.on(
    on_success=lambda a: print(f"Result: {a}"),
    on_failure=lambda e: print(f"Error: {e}"),
)
# ==> Will print "Result: 20"


```

### Either examples

```python
from pynction import left, right, Either


LESS_THAN_10_LETTERS = Literal["LESS_THAN_10_LETTERS"]
GREATER_THAN_100 = Literal["GREATER_THAN_100"]
WordTransformationError = Literal[LESS_THAN_10_LETTERS, GREATER_THAN_100]

def make_upper_case_first_n_letters(word: str, number: int) -> Either[WordTransformationError, str]:
    if len(word) < 10:
        return left("LESS_THAN_10_LETTERS")
    elif number > 100:
        return left("GREATER_THAN_100")
    else:
        return right(word.upper()[0:number])

result = make_upper_case_first_n_letters("example", 10)
print(result) # ==> Will be Left("LESS_THAN_10_LETTERS")
```

## API

### Stream

#### Factory methods

1. `stream(*args: T) -> Stream[T]`
2. `stream_of(elems: Iterable[T]) -> Stream[T]`

#### Stream api

1. `map(f: Callable[[T], S]) -> Stream[S]`
2. `filter(condition: Callable[[T], bool]) -> Stream[T]`
3. `flat_map(f: Callable[[T], Iterable[S]]) -> Stream[S]`
4. `take_while(condition: Callable[[T], bool]) -> Stream[T]`
5. `to_list() -> List[T]`
6. `to_set() -> Set[T]`

### Maybe

#### Factory methods

1. `maybe(elem: Optional[T]) -> Maybe[T]`
2. `just(elem: T) -> Just[T]`
3. `nothing`: It is a global instance of Nothing

#### Maybe api

1. `is_empty -> bool`
2. `map(f: Callable[[T], V]) -> Maybe[V]`
3. `flat_map(f: Callable[[T], Maybe[V]]) -> Maybe[V]`
4. `get_or_else(default: T) -> T`
5. `to_either(error: L) -> Either[L, T]`

### Either

#### Factory methods

1. `right(elem: T) -> Either[Any, T]`
2. `left(elem: T) -> Either[T, Any]`

#### Either api

1. `is_left -> bool`
2. `is_right -> bool`
3. `map(f: Callable[[R], R1]) -> Either[L, R1]`
4. `filter_or_else(predicate: Callable[[R], bool], leftValue: L) -> Either[L, R]`
5. `get_or_else_get(f: Callable[[L], R]) -> R`

### Try

#### Factory methods

1. `try_of(f: Callable[[], T]) -> Try[T]`

#### Try api

1. `map(f: Callable[[T], S]) -> Try[S]`
2. `flat_map(f: Callable[[T], Try[S]]) -> Try[S]`
3. `get_or_else_get(self, default: Callable[[Exception], T]) -> T`
4. `on( on_success: Callable[[T], None] = None, on_failure: Callable [[Exception], None] = None ) -> Try[T]`
5. `catch(f: Callable[[Exception], T]) -> Try[T]`
6. `and_finally(f: Callable[[], None]) -> Try[T]`
7. `to_either() -> Either[Exception, T]`

### Do notation

The following functions are python decorators that enables your decoratee function to use the `do` notation way of programming like Haskell or Scala. To better understand this decorators let's take a look at 2 quick examples

1. `do_either`

```python
@do_either
def example_with_union() -> DoEither[str, Union[int, str], str]:
    name = yield get_eihter_name()
    age = yield right(25)
    lastname = yield right("wick")
    return f"{name} {lastname} with age {age}"

result: Either[str, str] = example_with_union()
```

2. `do_maybe`

```python
@do_maybe
def do_maybe_example() -> DoMaybe[Union[str, int], str]:
    name = yield get_maybe_name()
    age = yield get_maybe_age()
    return f"{name} {age}"

result: Maybe[str] = do_maybe_example()
```
