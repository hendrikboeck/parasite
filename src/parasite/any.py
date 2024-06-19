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

    Inheritance:
        .. inheritance-diagram:: parasite.any.Any_
            :parts: 1
    """
    _f_optional: bool = False   # Whether the value is optional

    def __init__(self) -> None:
        pass

    def optional(self) -> Any_:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Any_: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.any().optional() })
                schema2 = p.obj({ "name": p.any() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": "John" })
                { "name": "John" }
                >>> schema.parse({ })
                { }

                >>> schema2.parse({ "name": "John" })
                { "name": "John" }
                >>> schema2.parse({ })
                ValidationError: key 'name' not found, but is required
        """
        self._f_optional = True
        return self

    def required(self) -> Any_:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`optional` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Any_: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.any().optional().required() })
                schema2 = p.obj({ "name": p.any() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": "John" })
                { "name": "John" }
                >>> schema.parse({ })
                ValidationError: key 'name' not found, but is required

                >>> schema2.parse({ "name": "John" })
                { "name": "John" }
                >>> schema2.parse({ })
                ValidationError: key 'name' not found, but is required
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

        raise ValidationError(f"key {key!r} not found, but is required")
