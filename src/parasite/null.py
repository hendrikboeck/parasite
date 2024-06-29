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
    ``parasite`` schema for ``None`` values.

    Note:
        Please use ``p.null()`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p

            schema = p.null()
            ...

    Inheritance:
        .. inheritance-diagram:: parasite.null.Null
            :parts: 1
    """

    _f_optional: bool = False  # Wether the value is optional

    def __init__(self) -> None:
        pass

    def optional(self) -> Null:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Null: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "null": p.null().optional() })
                schema2 = p.obj({ "null": p.null() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "null": None })
                { "null": None }
                >>> schema.parse({ })
                { }

                >>> schema2.parse({ "null": None })
                { "null": None }
                >>> schema2.parse({ })
                ValidationError: key "null" not found, but is required
        """
        self._f_optional = True
        return self

    def required(self) -> Null:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`optional` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Null: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "null": p.null().optional().required() })
                schema2 = p.obj({ "null": p.null() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "null": None })
                { "null": None }
                >>> schema.parse({ })
                ValidationError: key "null" not found, but is required

                >>> schema2.parse({ "null": None })
                { "null": None }
                >>> schema2.parse({ })
                ValidationError: key "null" not found, but is required
        """
        self._f_optional = False
        return self

    def parse(self, obj: Any) -> None:
        # do a loose comparison to None, to allow for subclasses of None
        if obj == None:  # noqa: E711
            return None

        # else raise an error
        raise ValidationError(f"object has to be None, but is {obj!r}")

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[None]:
        # if key is found, just package ``parse(..)`` it into a Some
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            return Some(self.parse(value))

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key {key!r} not found, but is required")
