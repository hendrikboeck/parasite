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

    Note:
        Please use ``p.null()`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p
            schema = p.null()
            ...
    """
    _f_optional: bool = False   # Wether the value is optional

    def __init__(self) -> None:
        pass

    def optional(self) -> Null:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Returns:
            Null: modified instance

        Example usage::

            from parasite import p

            schema = p.obj({ "name": p.null() })
            schema.parse({ "name": None })  # -> { "name": None }
            schema.parse({ })  # -> ValidationError: key 'name' not found, but is required

            schema = p.obj({ "name": p.null().optional() })
            schema.parse({ "name": None })  # -> { "name": None }
            schema.parse({ })  # -> { }
        """
        self._f_optional = True
        return self

    def required(self) -> Null:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Returns:
            Null: modified instance

        Example usage::

            from parasite import p

            schema = p.obj({ "name": p.null() })
            schema.parse({ "name": None })  # -> { "name": None }
            schema.parse({ })  # -> ValidationError: key 'name' not found, but is required

            schema = p.obj({ "name": p.null().required() })
            schema.parse({ "name": None })  # -> { "name": None }
            schema.parse({ })  # -> ValidationError: key 'name' not found, but is required
        """
        self._f_optional = False
        return self

    def parse(self, obj: Any) -> None:
        # if obj is None, return None
        if obj is None:
            return None

        # else raise an error
        raise ValidationError(f"object has to be None, but is '{obj!r}'")

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[None]:
        # if key is found, just package ``parse(..)`` it into a Some
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            return Some(self.parse(value))

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key '{key}' not found, but is required")
