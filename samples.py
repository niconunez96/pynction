from typing import Generator, List, Union

from typing_extensions import Literal, TypedDict

from pynction.either import DoEither, Either, Left, Right
from pynction.either import do as either_do
from pynction.maybe import Just, Maybe, Nothing, do
from pynction.stream import stream, stream_of
from pynction.try_monad import Try


# Maybe examples
def isEmpty(something: Maybe[str]) -> bool:
    return something.map(lambda s: s.upper()).is_empty


def sum10(something: Maybe[int]) -> int:
    return something.map(lambda a: a + 10).get_or_else(10)


def sum20(something: Maybe[int]) -> Either[str, int]:
    return something.map(lambda x: x + 20).to_either("NUMBER_NOT_FOUND")


print("*** Maybe samples ***")
print(isEmpty(Nothing()))
print(isEmpty(Just("something")))


print(sum10(Nothing()))
print(sum10(Just(10)))

# Either examples
LESS_THAN_10_LETTERS = Literal["LESS_THAN_10_LETTERS"]
CONTAINS_UPPERCASE_LETTERS = Literal["CONTAINS_UPPERCASE_LETTERS"]
Error = Literal[LESS_THAN_10_LETTERS, CONTAINS_UPPERCASE_LETTERS]

GREATER_THAN_100 = Literal["GREATER_THAN_100"]
NumberError = Literal[GREATER_THAN_100]


class Response(TypedDict):
    body: dict
    status: int


def make_upper_case_first_n_letters(
    word: str, number: int
) -> Either[Literal[Error, NumberError], str]:
    if len(word) < 10:
        return Left("LESS_THAN_10_LETTERS")
    elif number > 100:
        return Left("GREATER_THAN_100")
    elif word.isupper():
        return Left("CONTAINS_UPPERCASE_LETTERS")
    else:
        return Right(word.upper()[0:number])


def transform_word(word: str) -> Response:
    result = make_upper_case_first_n_letters(word, 10)

    def mapError(error: Literal[Error, NumberError]) -> Response:
        if error == "LESS_THAN_10_LETTERS":
            return {"body": {"error": "less than 10"}, "status": 400}
        elif error == "CONTAINS_UPPERCASE_LETTERS":
            return {"body": {"error": "contains upper case"}, "status": 400}
        elif error == "GREATER_THAN_100":
            return {"body": {"error": "number greater than 100"}, "status": 400}
        return {"body": {"error": "unexpected"}, "status": 500}

    return result.map(lambda s: Response(body={"data": s}, status=200)).get_or_else_get(
        lambda error: mapError(error)
    )


print("*** Either samples ***")
print(transform_word("NICOLAS ALEJANDRO NUNEZ"))


bar = stream([1, 2, 3, 4])
bax = stream_of([""])
baz = stream("12", "1")

# Stream example
foo: List[int] = stream(1, 2, 3, 4).to_list
bla = (
    stream_of([1, 2, 3, 4])
    .map(lambda a: a + 1)
    .filter(lambda n: n > 2)
    .flat_map(lambda n: [n, n * 2])
    .to_list
)
print("*** Stream samples ***")
print(bla)
print(foo)

# Try examples


def add_10(n: int) -> int:
    if n > 10:
        raise Exception("n must be less than 10")
    return n + 10


def handle_error(e: Exception) -> int:
    return -1


try_example = Try.of(lambda: add_10(11)).catch(handle_error).map(lambda a: a + 1)

try_example_2 = Try.of(lambda: add_10(11)).map(lambda a: a + 1)

try_example_3 = Try.of(lambda: add_10(9)).map(lambda a: a + 1)

print("*** Try samples ***")
try_example.on(lambda a: print(f"Result: {a}"), lambda e: print(f"Error: {e}"))
try_example_2.on(lambda a: print(f"Result: {a}"), lambda e: print(f"Error: {e}"))
try_example_3.on(lambda a: print(f"Result: {a}"), lambda e: print(f"Error: {e}"))


# Do notation maybe
def get_name() -> Maybe[str]:
    return Just("nicolas")


def get_age() -> Maybe[int]:
    return Just(10)


example: Maybe[str]
temp1 = get_name()
temp2 = get_age()
temp1.flat_map(lambda name: temp2.map(lambda surname: f"{name} {surname}"))

temp1.flat_map(lambda name: get_age().map(lambda surname: f"{name} {surname}"))


@do
def do_notation_example() -> Generator[Maybe[Union[str, int]], Union[str, int], str]:
    name = yield get_name()
    age = yield get_age()
    return f"{name} {age}"


value = do_notation_example()
print(value)


# Do notation for either
class User:
    name: str

    def __init__(self, name: str):
        self.name = name


def find_user(id: int) -> Maybe[User]:
    print(f"ID {id}")
    return Just(User(name="nicolas"))
    # return Nothing()


def execute_validation(user: User) -> Either[str, User]:
    return Right(user)
    # return Left("USER_DOES_NOT_HAVE_PERMS")


def execute_use_case(user: User) -> Either[str, User]:
    return Right(user)
    # return Left("INVALID_OPERATION")


@either_do
def either_do_example(id: int) -> DoEither[str, User, None]:
    user = yield find_user(id).to_either("USER_NOT_FOUND")
    user = yield execute_validation(user)
    user = yield execute_use_case(user)
    return None


def get_eihter_name() -> Either[str, str]:
    return Either.right("john")


@either_do
def example_with_union() -> DoEither[str, Union[int, str], str]:
    name = yield get_eihter_name()
    age = yield Right(25)
    lastname = yield Right("wick")
    return f"{name} {lastname} with age {age}"


result = either_do_example(1)
print(result)
