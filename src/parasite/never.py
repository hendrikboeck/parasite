# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass
from typing import Any, TypeVar

# -- Library Imports --
from rusttypes.option import Nil, Option

# -- Package Imports --
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class Never(ParasiteType[None]):
    """
    Parasite type for representing never values.

    Note:
        Please use ``p.never()`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p

            schema = p.never()
            ...
    """

    def __init__(self) -> None:
        pass

    def parse(self, obj: Any) -> None:
        # always raise an error, as this type can never be parsed
        raise ValidationError("this type can never be parsed")

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[None]:
        # if key is found, raise an error
        if parent.get(key, _NotFound) is not _NotFound:
            raise ValidationError(f"key {key!r} found, but this type can never be parsed")

        return Nil
