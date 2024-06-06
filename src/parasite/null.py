# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass
from typing import Any, TypeVar

# -- Library Imports --
from rusttypes.option import Nil, Option, Some

# -- Package Imports --
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class Null(ParasiteType[None]):
    """
    Parasite type for representing None values.

    Inheritance:
        ParasiteType[None]

    Args:
        _f_optional (bool): Whether the value is optional. Default: False
    """
    _f_optional: bool = False

    def optional(self) -> Null:
        """
        Makes the value optional, when parsing with `find_and_parse(..)`. Has no effect on
        `parse(..)`. Inverse of `required(..)`.

        Returns:
            Null: modified instance
        """
        self._f_optional = True
        return self

    def required(self) -> Null:
        """
        Makes the value required, when parsing with `find_and_parse(..)`. Has no effect on
        `parse(..)`. Default behavior. Inverse of `optional(..)`.

        Returns:
            Null: modified instance
        """
        self._f_optional = False
        return self

    def parse(self, obj: Any) -> None:
        # if obj is None, return None
        if obj is None:
            return None

        # else raise an error
        raise ValidationError(f"object has to be None, but is '{obj!r}'")

    def find_and_parse(self, parent: dict[K, Any], key: K) -> Option[None]:
        # if key is found, just package `parse(..)` it into a Some
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            return Some(self.parse(value))

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key '{key}' not found, but is required")
