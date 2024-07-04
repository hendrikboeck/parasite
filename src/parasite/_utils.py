from typing import Optional, TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")


def map_optional(func: Callable[[T], U], value: Optional[T]) -> Optional[U]:
    """
    Calls the mapping function on the value, if it is not None.

    Args:
        func (callable[[T], U]): mapping function
        value (Optional[T]): value to map

    Returns:
        Optional[U]: mapped value
    """
    if value is None:
        return value

    return func(value)
