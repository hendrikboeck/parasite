# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass, field
from typing import Any, Iterable, TypeVar

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
    Parasite type for representing variant values. The value can be one of the variants specified in
    the constructor or added through the :func:`add_item` function. The value is parsed by trying to
    parse it with each variant in the order they are added. If note of the variants can parse the
    value, a :class:`ValidationError` is raised.
    """
    # The variants of the variant.
    _m_variants: list[ParasiteType] = field(default_factory = lambda: [])

    _f_optional: bool = False   # Whether the value is optional.
    _f_nullable: bool = False   # Whether the value can be None.

    def __init__(self, variants: Iterable[ParasiteType] = []):
        """
        Args:
            variants (Iterable[ParasiteType], optional): The variants of the variant. Default: [].

        Example usage:
            You can create a variant schema by passing the variants as a list to the constructor.
            The variants can be any of the parasite types. The following example shows how to create
            a variant schema with a string and an integer variant::

                from parasite import p

                schema = p.variant([
                    p.string(),
                    p.number().integer(),
                ])

                schema2 = p.variant()

            The resulting schemas will parse the following objects::

                >>> schema.parse("42")
                "42"
                >>> schema.parse(42)
                42

                >>> schema2.parse("42")
                ValidationError: object has to be one of [], but is "42"

        """
        self._m_variants = list(variants)

    def optional(self) -> Variant:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Variant: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ]).optional()
                })

                schema2 = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ])
                })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": "42" })
                { "sub": "42" }
                >>> schema.parse({ })
                { }

                >>> schema2.parse({ "sub": 42 })
                { "sub": 42 }
                >>> schema2.parse({ })
                ValidationError: key 'sub' not found, but is required
        """
        self._f_optional = True
        return self

    def required(self) -> Variant:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`optional` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Variant: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ]).optional().required()
                })

                schema2 = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ])
                })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": "42" })
                { "sub": "42" }
                >>> schema.parse({ })
                ValidationError: key 'sub' not found, but is required

                >>> schema2.parse({ "sub": 42 })
                { "sub": 42 }
                >>> schema2.parse({ })
                ValidationError: key 'sub' not found, but is required
        """
        self._f_optional = False
        return self

    def nullable(self) -> Variant:
        """
        Makes the value nullable, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`not_nullable`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Variant: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ]).nullable()
                })

                schema2 = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ])
                })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": "42" })
                { "sub": "42" }
                >>> schema.parse({ "sub": None })
                { "sub": None }

                >>> schema2.parse({ "sub": 42 })
                { "sub": 42 }
                >>> schema2.parse({ "sub": None })
                ValidationError: object has to be a dictionary, but is 'None'
        """
        self._f_nullable = True
        return self

    def not_nullable(self) -> Variant:
        """
        Makes the value not-nullable, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`nullable`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`nullable` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Variant: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ]).nullable().not_nullable()
                })

                schema2 = p.obj({
                    "sub": p.variant([
                        p.string(),
                        p.number().integer(),
                    ])
                })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": "42" })
                { "sub": "42" }
                >>> schema.parse({ "sub": None })
                ValidationError: key 'sub' cannot be None

                >>> schema2.parse({ "sub": 42 })
                { "sub": 42 }
                >>> schema2.parse({ "sub": None })
                ValidationError: key 'sub' not found, but is required
        """
        self._f_nullable = False
        return self

    def add_variant(self, variant: ParasiteType) -> Variant:
        """
        Add a variant to the variant.

        Note:
            The order of the variants is important, as the value is parsed by trying to parse it
            with each variant in the order they are added. The first variant that can parse the
            value is used.

        Args:
            variant (ParasiteType): The variant to add.

        Returns:
            Variant: The updated instance of the class.

        Example usage:
            You can add a variant to the variant by calling the :func:`add_variant` function. The
            following example shows how to add a string variant to a variant schema::

                from parasite import p

                schema = p.variant()
                schema.add_variant(p.string())

            The resulting schema will parse the following objects::

                >>> schema.parse("42")
                "42"

                >>> schema.parse(42)
                ValidationError: object has to be one of [String(...)], but is 42
        """
        self._m_variants.append(variant)
        return self

    def rm_variant(self, variant: ParasiteType) -> Variant:
        """
        Remove a variant from the variant.

        Warning:
            The variant is removed by reference, so the variant has to be the same instance as the
            one added to the variant. Equivalent ro the ``list.remove`` function.

        Throws:
            ValueError: If the variant is not found in the variant.

        Args:
            variant (ParasiteType): The variant to remove.

        Returns:
            Variant: The updated instance of the class.

        Example usage:
            You can remove a variant from the variant by calling the :func:`rm_variant` function.
            The following example shows how to remove a string variant from a variant schema::

                from parasite import p

                schema = p.variant([
                    p.string(),
                    p.number().integer(),
                ])
                schema.rm_variant(p.string())

            The resulting schema will parse the following objects::

                >>> schema.parse(42)
                42

                >>> schema.parse("42")
                ValidationError: object has to be one of [Number(...)], but is '42'
        """
        try:
            self._m_variants.remove(variant)
        except ValueError as exc:
            raise ValueError(f"Variant {variant!r} not found in {self!r}") from exc

        return self

    def rm_variant_safe(self, variant: ParasiteType) -> Result[Variant, ValueError]:
        """
        Remove a variant from the variant.

        Warning:
            The variant is removed by reference, so the variant has to be the same instance as the
            one added to the variant. Equivalent ro the ``list.remove`` function.

        Args:
            variant (ParasiteType): The variant to remove.

        Returns:
            Result[Variant, ValueError]: The updated instance of the class or an error

        Example usage:
            You can remove a variant from the variant by calling the :func:`rm_variant_safe` function.
            The following example shows how to remove a string variant from a variant schema::

                from parasite import p

                schema = (
                    p.variant([
                        p.string(),
                        p.number().integer(),
                    ])
                    .rm_variant_safe(p.string())
                    .expect("Variant not found")
                )

            The resulting schema will parse the following objects::

                >>> schema.parse(42)
                42

                >>> schema.parse("42")
                ValidationError: object has to be one of [Number(...)], but is '42'

            If the variant is not found, an error is returned::

                >>> schema.rm_variant_safe(p.string())
                Err(ValueError: "Variant String(...) not found in Variant(...)")
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
