from time import time

from pynction import stream_of

# mypy: ignore-errors


def timer(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} took {end-start} seconds")
        return result

    return wrapper


@timer
def pythonic_way(elem_quantity):
    temp = [number * 2 for number in range(elem_quantity) if number % 2 == 0]
    temp2 = []
    for n in temp:
        temp2.extend([n + 1, n + 2])
    result = []
    for n in temp2:
        if n > 1000:
            break
        result.append(n)
    print("Pythonic result: ", len(result))


@timer
def python_itertools_way(elem_quantity):
    temp = filter(lambda x: x % 2 == 0, range(elem_quantity))
    temp2 = map(lambda a: a * 2, temp)
    temp3 = []
    for n in temp2:
        temp3.extend([n + 1, n + 2])
    result = []
    for n in temp3:
        if n > 1000:
            break
        result.append(n)
    print("Itetools result: ", len(result))


@timer
def pynction_way(elem_quantity):
    result = (
        stream_of(range(elem_quantity))
        .filter(lambda x: x % 2 == 0)
        .map(lambda a: a * 2)
        .flat_map(lambda a: [a + 1, a + 2])
        .take_while(lambda a: a < 1000)
        .to_list
    )
    print("Pynction result: ", len(result))


if __name__ == "__main__":
    """
    3 functions that do:
        - Filter even numbers
        - Duplicate them
        - Obtain the next 2 numbers of each number
    """
    print("Pythonic way:")
    pythonic_way(10000000)
    print("Itertools way:")
    python_itertools_way(10000000)
    print("Pynction way:")
    pynction_way(10000000)
