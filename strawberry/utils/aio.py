import itertools
import sys
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any, AsyncIterable, List, Optional, Tuple, TypeVar, Union

itertools.islice
_T = TypeVar("_T")


async def aenumerate(
    iterable: Union[AsyncIterator[_T], AsyncIterable[_T]],
) -> AsyncIterator[Tuple[int, _T]]:
    """Async version of enumerate."""
    i = 0
    async for element in iterable:
        yield i, element
        i += 1


async def aislice(
    aiterable: Union[AsyncIterator[_T], AsyncIterable[_T]],
    start: Optional[int] = None,
    stop: Optional[int] = None,
    step: Optional[int] = None,
) -> AsyncIterator[_T]:
    """Async version of itertools.islice."""
    # This is based on
    it = iter(range(start or 0, stop or sys.maxsize, step or 1))
    try:
        nexti = next(it)
    except StopIteration:
        return

    try:
        async for i, element in aenumerate(aiterable):
            if i == nexti:
                yield element
                nexti = next(it)
    except StopIteration:
        return


async def asyncgen_to_list(generator: AsyncGenerator[_T, Any]) -> List[_T]:
    """Convert an async generator to a list."""
    return [element async for element in generator]
