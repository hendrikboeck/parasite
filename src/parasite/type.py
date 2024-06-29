# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

# -- Library Imports --
from rusttypes.option import Option
from rusttypes.result import Err, Ok, Result

# -- Package Imports --
from parasite.errors import ValidationError

T = TypeVar("T")
"""Template type for the destination value."""

K = TypeVar("K")
"""Template type for the key in a dictionary."""

_NotFound = object()
"""Internal parasite value for not found keys."""


@dataclass
class ParasiteType(ABC, Generic[T]):
    """
    Abstract base class for parasite types. Parasite types are used to parse and validate values
    from a dictionary or standalone values (some options are only available for dictionaries).

    Inheritance:
        .. inheritance-diagram:: parasite.type.ParasiteType
            :parts: 1
    """

    @abstractmethod
    def parse(self, obj: Any) -> T:
        """
        Default method for parsing a value. This method should be overridden by subclasses.

        Throws:
            ValidationError: if the value could not be parsed or was invalid

        Args:
            obj (Any): value to parse

        Returns:
            T: parsed destination value
        """
        raise NotImplementedError

    @abstractmethod
    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[T | None]:
        """
        Default method for finding and parsing a value from a dictionary. This method should be
        overridden by subclasses. If the key is not found, the method should return :class:`Nil`.

        Throws:
            ValidationError: if the value could not be parsed or was invalid

        Args:
            parent (dict[K, Any]): dictionary to search for the key
            key (K): key to search for in the dictionary

        Returns:
            Option[T]: parsed destination value or ``Nil``
        """
        raise NotImplementedError

    def parse_safe(self, obj: Any) -> Result[T, ValidationError]:
        """
        Converts the result of :func:`parse` into a :class:`rusttypes.result.Result` type. Should be
        used when safe parsing is required.

        Note:
            Will only catch :class:`parasite.errors.ValidationError` exceptions!!!

        Args:
            obj (Any): value to parse

        Returns:
            Result[T, ValidationError]: parsed destination value or an error
        """
        try:
            # may throw a ValidationError exception
            return Ok(self.parse(obj))

        # handle ValidationError exceptions, if parsing fails
        except ValidationError as exc:
            return Err(exc)

    def _find_and_parse_safe(
        self,
        parent: dict[K, Any],
        key: K,
    ) -> Result[Option[T | None], ValidationError]:
        """
        Converts the result of :func:`_find_and_parse` into a ``Result`` type. Should be used when
        safe parsing is required.

        Note:
            Will only catch :class:`parasite.errors.ValidationError` exceptions!!!

        Args:
            parent (dict[K, Any]): dictionary to search for the key
            key (K): key to search for in the dictionary

        Returns:
            Result[T, ValidationError]: parsed destination value or an error
        """
        try:
            # may throw a ValidationError exception
            return Ok(self._find_and_parse(parent, key))

        # handle ValidationError exceptions, if parsing fails
        except ValidationError as exc:
            return Err(exc)
