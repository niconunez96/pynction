from typing import Generic, NamedTuple, Optional, Tuple, TypeVar, Callable, Any
from typing_extensions import Literal, TypedDict
from enum import Enum


L = TypeVar("L")
L1 = TypeVar("L1")
R = TypeVar("R")
R1 = TypeVar("R1")


class Either(Generic[L, R]):
    def is_left(self) -> bool:
        pass
    
    def is_right(self) -> bool:
        pass

    def map(self, f: Callable[[R], R1]) -> 'Either[L, R1]':
        pass

    def filter_or_else(self, predicate: Callable[[R], bool], leftValue: L) -> 'Either[L, R]':
        pass

    def get_or_else_get(self, f: Callable[[L], R]) -> R:
        pass


class Right(Either[L, R]):
    value: R
    def __init__(self, value: R):
        self.value = value

    def is_left(self) -> bool:
        return False
    
    def is_right(self) -> bool:
        return True

    def map(self, f: Callable[[R], R1]) -> 'Right[L, R1]':
        return Right(f(self.value))
    
    def filter_or_else(self, satisfyCondition: Callable[[R], bool], leftValue: L) -> 'Either[L, R]':
        if satisfyCondition(self.value):
            return self
        else:
            return Left(leftValue)

    def get_or_else_get(self, _: Callable[[L], R]) -> R:
        return self.value


class Left(Either[L, R]):
    value: L
    def __init__(self, value: L):
        self.value = value

    def is_left(self) -> bool:
        return True
    
    def is_right(self) -> bool:
        return False
    
    def map(self, _: Callable[[R], R1]) -> 'Left[L, R1]':
        return Left[L, R1](self.value)
    
    def filter_or_else(self, _: Callable[[R], bool], _1: L) -> 'Left[L, R]':
        return self
    
    def get_or_else_get(self, f: Callable[[L], R]) -> R:
        return f(self.value)



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
        return Right(word.upper()[0: number])


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

    return result.map(
        lambda s: Response(body={'data': s}, status=200)
    ).get_or_else_get(lambda error: mapError(error))


print(transform_word("NICOLAS ALEJANDRO NUNEZ"))
