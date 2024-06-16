# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass, field
from typing import Any, TypeVar

# -- Library Imports --
from rusttypes.option import Nil, Option, Some
from rusttypes.result import Result, Err, Ok

# -- Package Imports --
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class Variant(ParasiteType[Any]):
    """
    Parasite type for representing variant values.

    Inheritance:
        ParasiteType[Any]

    Args:
        _f_optional (bool): Whether the value is optional. Default: False
        _f_nullable (bool): Whether the value can be None. Default: False
        _m_variants (set[ParasiteType]): The variants of the variant. Default: {}
    """
    # NOTE: do not move this attribute, this has to be first in the class, as it will break, reading
    # variants from list functionality
    _m_variants: list[ParasiteType] = field(default_factory = lambda: [])

    _f_optional: bool = False
    _f_nullable: bool = False

    def optional(self) -> Variant:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Returns:
            Variant: The updated instance of the class.
        """
        self._f_optional = True
        return self

    def required(self) -> Variant:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Returns:
            Variant: The updated instance of the class.
        """
        self._f_optional = False
        return self

    def nullable(self) -> Variant:
        """
        Set the value to be nullable.

        Returns:
            Variant: The updated instance of the class.
        """
        self._f_nullable = True
        return self

    def non_nullable(self) -> Variant:
        """
        Set the value to be non-nullable.

        Returns:
            Variant: The updated instance of the class.
        """
        self._f_nullable = False
        return self

    def add_variant(self, variant: ParasiteType) -> Variant:
        """
        Add a variant to the variant.

        Args:
            variant (ParasiteType): The variant to add.

        Returns:
            Variant: The updated instance of the class.
        """
        self._m_variants.append(variant)
        return self

    def rm_variant(self, variant: ParasiteType) -> Variant:
        """
        Remove a variant from the variant.

        Throws:
            ValueError: If the variant is not found in the variant.

        Args:
            variant (ParasiteType): The variant to remove.

        Returns:
            Variant: The updated instance of the class.
        """
        try:
            self._m_variants.remove(variant)
        except ValueError as exc:
            raise ValueError(f"Variant {variant!r} not found in {self!r}") from exc

        return self

    def rm_variant_safe(self, variant: ParasiteType) -> Result[Variant, ValueError]:
        """
        Remove a variant from the variant.

        Returns:
            Optional[ParasiteType]: The removed variant.
        """
        try:
            self.rm_variant(variant)
            return Ok(self)

        except ValueError as exc:
            return Err(exc)

    def parse(self, obj: Any) -> Any:
        for variant in self._m_variants:
            try:
                return variant.parse(obj)

            except ValidationError:
                continue

        raise ValidationError(f"object has to be one of {self._m_variants!r}, but is '{obj!r}'")

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[Any | None]:
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            # if key is found, just package ``parse(..)`` it into a Some
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
