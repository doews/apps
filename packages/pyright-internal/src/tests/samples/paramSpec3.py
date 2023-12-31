# This sample tests ParamSpec (PEP 612) behavior.

from typing import Awaitable, Callable, Generic, ParamSpec, TypeVar, overload

P = ParamSpec("P")
R = TypeVar("R")


def decorator1(f: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(*args, **kwargs)

    return inner


@decorator1
def func1(x: int, y: str) -> int:
    return x + 7


async def func2():
    await func1(1, "A")

    # This should generate an error because
    # the first parameter is not an int.
    await func1("B", "2")


@overload
def func3(x: int) -> None:
    ...


@overload
def func3(x: str) -> str:
    ...


def func3(x: int | str) -> str | None:
    if isinstance(x, int):
        return None
    else:
        return x


reveal_type(
    decorator1(func3),
    expected_text="Overload[(x: int) -> Awaitable[None], (x: str) -> Awaitable[str]]",
)


class ClassA(Generic[P, R]):
    def __init__(self, func: Callable[P, R]):
        self.func = func


def func4(f: Callable[P, R]) -> ClassA[P, R]:
    return ClassA(f)
