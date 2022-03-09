# Pynction 🐍
[![continuous_integration](https://github.com/niconunez96/pynction/actions/workflows/ci.yaml/badge.svg)](https://github.com/niconunez96/pynction/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/niconunez96/pynction/branch/main/graph/badge.svg?token=YI2ZOWV29E)](https://codecov.io/gh/niconunez96/pynction)

Functional based library to support haskell monads like Either, Maybe in
a scala fashion style. The library also contains Try monad inspired from vavr
and a Stream class which is pretty similar to scala and java stream API

## Why should you use it ?
TBD

## Samples

### Stream examples
```python
from pynction.stream import Stream


foo = (
    Stream.of([1, 2, 3, 4])
    .map(lambda a: a + 1)
    .filter(lambda n: n % 2 == 0)
    .flat_map(lambda n: [n, n * 2])
    .to_list
)

# foo => [2, 4, 4, 8]

bar = (
    Stream("example", "e", "something")
    .take_while(lambda s: s.startswith("e"))
    .to_list
)

# bar => ["example", "e"]
```
### Maybe examples
```python
from pynction.maybe import Maybe, Nothing, Just

def divide_10_by(n: int) -> Maybe[int]:
    if n == 0:
        return Nothing()
    return Just(10 / n)

result = divide_10_by(2).get_or_else_get(-1)
# result => 5
result = divide_10_by(0).get_or_else_get(-1)
# result => -1
```
```python
from pynction.maybe import Maybe


class User:
    id: int
    name: str


def find_user(id: int) -> Maybe[User]:
    # Examples purposes
    return Just(User(id)) if id % 2 == 0 else Nothing()

username_or_error: Either[str, str] = (
    find_user(2)
    .map(lambda u: u.name)
    .to_either("USER_NOT_FOUND")
)
```
### Try examples
```python
from pynction.try_monad import Try


def add_10(n: int) -> int:
    if n > 10:
        raise Exception("n must be less than 10")
    return n + 10

try_example = Try.of(lambda: add_10(11)).catch(lambda exc: -1)
try_example.on(lambda a: print(f"Result: {a}"), lambda e: print(f"Error: {e}"))
# ==> Will print "Result: -1"


try_example_2 = Try.of(lambda: add_10(11)).map(lambda a: a + 1)
try_example_2.on(lambda a: print(f"Result: {a}"), lambda e: print(f"Error: {e}"))
# ==> Will print "Error: n must be less than 10"

try_example_3 = Try.of(lambda: add_10(9)).map(lambda a: a + 1)
try_example_3.on(lambda a: print(f"Result: {a}"), lambda e: print(f"Error: {e}"))
# ==> Will print "Result: 20"


```
### Either examples
```python
### This example illustrates how a controller can handle an Either response from the "application" layer ###

## Application layer

LESS_THAN_10_LETTERS = Literal["LESS_THAN_10_LETTERS"]
CONTAINS_UPPERCASE_LETTERS = Literal["CONTAINS_UPPERCASE_LETTERS"]
GREATER_THAN_100 = Literal["GREATER_THAN_100"]
WordTransformationError = Literal[LESS_THAN_10_LETTERS, CONTAINS_UPPERCASE_LETTERS, GREATER_THAN_100]

def make_upper_case_first_n_letters(word: str, number: int) -> Either[WordTransformationError, str]:
    if len(word) < 10:
        return Left("LESS_THAN_10_LETTERS")
    elif number > 100:
        return Left("GREATER_THAN_100")
    elif word.isupper():
        return Left("CONTAINS_UPPERCASE_LETTERS")
    else:
        return Right(word.upper()[0:number])


## Controller layer

class Response(TypedDict):
    body: dict
    status: int

@get
def transform_word(word: str) -> Response:
    def mapError(error: Literal[Error, NumberError]) -> Response:
        if error == "LESS_THAN_10_LETTERS":
            return {"body": {"error": "less than 10"}, "status": 400}
        elif error == "CONTAINS_UPPERCASE_LETTERS":
            return {"body": {"error": "contains upper case"}, "status": 400}
        elif error == "GREATER_THAN_100":
            return {"body": {"error": "number greater than 100"}, "status": 400}
        return {"body": {"error": "unexpected"}, "status": 500}

    result = make_upper_case_first_n_letters(word, 10)

    return result.map(lambda s: Response(body={"data": s}, status=200)).get_or_else_get(
        lambda error: mapError(error)
    )
```

## API

### Stream
### Maybe
### Either
### Try
