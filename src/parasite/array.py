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
    Parasite type for representing list values.

    Inheritance:
        ParasiteType[list]

    Args:
        _f_optional (bool): Whether the value is optional. Default: False
        _f_nullable (bool): Whether the value can be None. Default: False
        _m_ul (int | None): The upper limit of the list. Default: None
        _m_ll (int | None): The lower limit of the list. Default: None
        _m_element (ParasiteType[T] | None): The element type of the list. Default: None
    """
    # NOTE: do not move this attribute, this has to be first in the class, as it will break, reading
    # element from constructor functionality
    _m_element: ParasiteType | None = None

    _f_optional: bool = False
    _f_nullable: bool = False

    _m_ul: int | None = None
    _m_ll: int | None = None

    def optional(self) -> Array:
        """
        Set the value to be optional.

        Returns:
            Array: The updated instance of the class.
        """
        self._f_optional = True
        return self

    def required(self) -> Array:
        """
        Set the value to be required.

        Returns:
            Array: The updated instance of the class.
        """
        self._f_optional = False
        return self

    def nullable(self) -> Array:
        """
        Set the value to be nullable.

        Returns:
            Array: The updated instance of the class.
        """
        self._f_nullable = True
        return self

    def non_nullable(self) -> Array:
        """
        Set the value to be non-nullable.

        Returns:
            Array: The updated instance of the class.
        """
        self._f_nullable = False
        return self

    def min(self, value: int) -> Array:
        """
        Set the minimum length of the list.

        Args:
            value (int): The minimum length of the list.

        Returns:
            Array: The updated instance of the class.
        """
        self._m_ll = value
        return self

    def max(self, value: int) -> Array:
        """
        Set the maximum length of the list.

        Args:
            value (int): The maximum length of the list.

        Returns:
            Array: The updated instance of the class.
        """
        self._m_ul = value
        return self

    def not_empty(self) -> Array:
        """
        Set the list to not be empty.

        Returns:
            Array: The updated instance of the class.
        """
        return self.min(1)

    def empty(self) -> Array:
        """
        Set the list to be empty.

        Returns:
            Array: The updated instance of the class.
        """
        return self.max(0)

    def length(self, value: int) -> Array:
        """
        Set the length of the list.

        Args:
            value (int): The length of the list.

        Returns:
            Array: The updated instance of the class.
        """
        return self.min(value).max(value)

    def element(self, element: ParasiteType) -> Array:
        """
        Set the element type of the list.

        Args:
            element (ParasiteType[T]): The element type of the list.

        Returns:
            Array: The updated instance of the class.
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

    def find_and_parse(self, parent: dict[K, Any], key: K) -> Option[list[Any] | None]:
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            # if key is found, just package `parse(..)` it into a Some
            if value is not None:
                return Some(self.parse(value))

            # if value is None, check if the value is nullable
            if self._f_nullable:
                return Some(None)

            raise ValidationError(f"key '{key}' cannot be None")

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key '{key}' not found, but is required")
