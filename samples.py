from typing import List
from typing_extensions import Literal, TypedDict
from fython.maybe import Maybe, Nothing, Just
from fython.either import Either, Left, Right
from fython.stream import Stream


# Maybe samples
def isEmpty(something: Maybe[str]) -> bool:
    return something.map(lambda s: s.upper()).is_empty()


def sum10(something: Maybe[int]) -> int:
    return something.map(lambda a: a + 10).get_or_else(10)


def sum20(something: Maybe[int]) -> Either[str, int]:
    return something.map(lambda x: x + 20).to_either("NUMBER_NOT_FOUND")


print("*** Maybe samples ***")
print(isEmpty(Nothing()))
print(isEmpty(Just("something")))


print(sum10(Nothing()))
print(sum10(Just(10)))

# Either samples
LESS_THAN_10_LETTERS = Literal["LESS_THAN_10_LETTERS"]
CONTAINS_UPPERCASE_LETTERS = Literal["CONTAINS_UPPERCASE_LETTERS"]
Error = Literal[LESS_THAN_10_LETTERS, CONTAINS_UPPERCASE_LETTERS]

GREATER_THAN_100 = Literal["GREATER_THAN_100"]
NumberError = Literal[GREATER_THAN_100]


class Response(TypedDict):
    body: dict
    status: int


def make_upper_case(word: str, number: int) -> Either[Literal[Error, NumberError], str]:
    if len(word) < 10:
        return Left("LESS_THAN_10_LETTERS")
    elif word.isupper():
        return Left("CONTAINS_UPPERCASE_LETTERS")
    elif number > 100:
        return Left("GREATER_THAN_100")
    else:
        return Right(word.upper()[0:number])


def transform_word(word: str) -> Response:
    result = make_upper_case(word, 10)

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


# Stream example
foo: List[int] = Stream(1, 2, 3, 4).to_list
bla = (
    Stream.of([1, 2, 3, 4])
    .map(lambda a: a + 1)
    .filter(lambda n: n > 2)
    .flat_map(lambda n: [n, n * 2])
    .to_list
)
print("*** Stream samples ***")
print(bla)
print(foo)
