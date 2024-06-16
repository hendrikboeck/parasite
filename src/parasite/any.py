# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass
from typing import Any, TypeVar

# -- Library Imports --
from rusttypes.option import Nil, Some, Option

# -- Package Imports --
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class Any_(ParasiteType[Any]):
    """
    Parasite type for representing any values. This is the default type, when no other type is
    specified.

    Note:
        Please use ``p.any()`` instead of instantiating this class directly. ``p`` can be imported
        with::

            from parasite import p
            schema = p.any()
            ...
    """
    _f_optional: bool = False   # Whether the value is optional

    def __init__(self) -> None:
        pass

    def optional(self) -> Any_:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Returns:
            Any_: modified instance

        Example usage::

            from parasite import p

            schema = p.obj({ "name": p.any() })
            schema.parse({ "name": "John" })  # -> { "name": "John" }
            schema.parse({ })  # -> ValidationError: key 'name' not found, but is required

            schema = p.obj({ "name": p.any().optional() })
            schema.parse({ "name": "John" })  # -> { "name": "John" }
            schema.parse({ })  # -> { }
        """
        self._f_optional = True
        return self

    def required(self) -> Any_:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Returns:
            Any_: modified instance

        Example usage::

            from parasite import p

            schema = p.obj({ "name": p.any() })
            schema.parse({ "name": "John" })  # -> { "name": "John" }
            schema.parse({ })  # -> ValidationError: key 'name' not found, but is required

            schema = p.obj({ "name": p.any().required() })
            schema.parse({ "name": "John" })  # -> { "name": "John" }
            schema.parse({ })  # -> ValidationError: key 'name' not found, but is required
        """
        self._f_optional = False
        return self

    def parse(self, obj: Any) -> Any:
        # can never fail, as it accepts any value
        return obj

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[Any]:
        # if key is found, just package ``parse(..)`` it into a Some
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            return Some(self.parse(value))

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key '{key}' not found, but is required")
