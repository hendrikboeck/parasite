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
class Array(ParasiteType[list[Any]]):
    """
    ``parasite`` type for creating and parsing list/array based schemas. Will return a python
    ``list[Any]`` with the parsed values on success.

    Note:
        Please use ``p.array(...)`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p
            schema = p.array(...)
            ...

    Note:
        Calling the constructor with an element type will set the element type of the list. This is
        equivalent to calling ``p.array().element(element)`` (see :func:`element`). If no element
        type is specified, the list will skip parsing the elements, and therefore accept any type of
        object or value.

    Inheritance:
        .. inheritance-diagram:: parasite.array.Array
            :parts: 1
    """
    _m_element: ParasiteType | None = None   # The element type of the list.

    _f_optional: bool = False   # Whether the value is optional.
    _f_nullable: bool = False   # Whether the value can be None.

    _m_ul: int | None = None   # The upper limit of the list.
    _m_ll: int | None = None   # The lower limit of the list.

    def __init__(self, element: ParasiteType | None = None):
        """
        Args:
            element (ParasiteType | None): The element type of the list. Default: None

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array()
                schema2 = p.array(p.string())

            The resulting schemas will parse the following objects::

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]
                >>> schema.parse(["John", 1])
                ["John", 1]

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]
                >>> schema.parse(["John", 1])
                ValidationError: element at index 1 is invalid: object has to be a string, but is 1
        """
        self.element(element)

    def optional(self) -> Array:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.array().optional() })
                schema2 = p.obj({ "name": p.array() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema.parse({ })
                { }

                >>> schema2.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema2.parse({ })
                ValidationError: key 'name' not found, but is required
        """
        self._f_optional = True
        return self

    def required(self) -> Array:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`optional` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.array().optional().required() })
                schema2 = p.obj({ "name": p.array()})

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema.parse({ })
                ValidationError: key 'name' not found, but is required

                >>> schema2.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema2.parse({ })
                ValidationError: key 'name' not found, but is required
        """
        self._f_optional = False
        return self

    def nullable(self) -> Array:
        """
        Makes the value nullable, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`not_nullable`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.array().nullable()})
                schema2 = p.obj({ "name": p.array() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema.parse({ "name": None })
                { "name": None }

                >>> schema2.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema2.parse({ "name": None })
                ValidationError: key "name" is not nullable, but is None
        """
        self._f_nullable = True
        return self

    def not_nullable(self) -> Array:
        """
        Makes the value not-nullable, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`nullable`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`nullable` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.array().nullable().not_nullable() })
                schema2 = p.obj({ "name": p.array() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema.parse({ "name": None })
                ValidationError: key "name" is not nullable, but is None

                >>> schema2.parse({ "name": ["John", "Doe"] })
                { "name": ["John", "Doe"] }
                >>> schema2.parse({ "name": None })
                ValidationError: key "name" is not nullable, but is None
        """
        self._f_nullable = False
        return self

    def min(self, value: int) -> Array:
        """
        Enforce the minimum length of the list.

        Args:
            value (int): The minimum length of the list.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array().min(2)

            The resulting schemas will parse the following objects::

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]

                >>> schema.parse(["John"])
                ValidationError: list has to have at least 2 elements, but has 1
        """
        self._m_ll = value
        return self

    def max(self, value: int) -> Array:
        """
        Enforce the maximum length of the list.

        Args:
            value (int): The maximum length of the list.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array().max(2)

            The resulting schemas will parse the following objects::

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]

                >>> schema.parse(["John", "Doe", "Smith"])
                ValidationError: list has to have at most 2 elements, but has 3
        """
        self._m_ul = value
        return self

    def not_empty(self) -> Array:
        """
        Enforce the list to not be empty. Equivalent to calling ``min(1)``.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array().not_empty()

            The resulting schemas will parse the following objects::

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]

                >>> schema.parse([ ])
                ValidationError: list has to have at least 1 elements, but has 0
        """
        return self.min(1)

    def empty(self) -> Array:
        """
        Enforce the list to be empty. Equivalent to calling ``max(0)``.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array().empty()

            The resulting schemas will parse the following objects::

                >>> schema.parse([ ])
                [ ]

                >>> schema.parse(["John", "Doe"])
                ValidationError: list has to have at most 0 elements, but has 2
        """
        return self.max(0)

    def length(self, value: int) -> Array:
        """
        Enforce the list to have exactly the given length. Equivalent to calling
        ``min(value).max(value)``.

        Args:
            value (int): The length of the list.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array().length(2)

            The resulting schemas will parse the following objects::

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]

                >>> schema.parse(["John", "Doe", "Smith"])
                ValidationError: list has to have exactly 2 elements, but has 3

                >>> schema.parse(["John"])
                ValidationError: list has to have exactly 2 elements, but has 1
        """
        return self.min(value).max(value)

    def element(self, element: ParasiteType) -> Array:
        """
        Set the ParsiteType schema of the elements in the list. Can also be set in the constructor.
        Note:
            If not set, the list will skip parsing the elements, and therefore accept any type of
            object or value.

        Args:
            element (ParasiteType[T]): The element type of the list.

        Returns:
            Array: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.array().element(p.string())

            The resulting schemas will parse the following objects::

                >>> schema.parse(["John", "Doe"])
                ["John", "Doe"]

                >>> schema.parse(["John", 1])
                ValidationError: element at index 1 is invalid: object has to be a string, but is 1
        """
        self._m_element = element
        return self

    def parse(self, obj: Any) -> list[Any]:
        if not isinstance(obj, list):
            raise ValidationError(f"object has to be a list, but is '{obj!r}'")

        if self._m_ll is not None and len(obj) < self._m_ll:
            raise ValidationError(
                f"list has to have at least {self._m_ll} elements, but has {len(obj)}"
            )

        if self._m_ul is not None and len(obj) > self._m_ul:
            raise ValidationError(
                f"list has to have at most {self._m_ul} elements, but has {len(obj)}"
            )

        if self._m_element is not None:
            # create a cache to not overwrite the original list on error
            cache = []

            # parse each element individually
            for i, element in enumerate(obj):
                try:
                    # may throw a ValidationError exception
                    cache.append(self._m_element.parse(element))

                # handle ValidationError exceptions, if parsing fails
                except ValidationError as exc:
                    raise ValidationError(f"element at index {i} is invalid: {exc}") from exc

            # if the parsing was successful, overwrite the original list
            obj = cache

        return obj

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[list[Any] | None]:
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            # if key is found, just package ``parse(..)`` it into a Some
            if value is not None:
                return Some(self.parse(value))

            # if value is None, check if the value is nullable
            if self._f_nullable:
                return Some(None)

            raise ValidationError(f"key '{key}' is not nullable, but is None")

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key '{key}' not found, but is required")
