# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass
import math
import re
from typing import Any, Optional, TypeVar

# -- Library Imports --
from rusttypes.option import Nil, Option, Some

# -- Package Imports --
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class Boolean(ParasiteType[bool]):
    """
    Parasite type for representing boolean values.

    Note:
        Please use ``p.boolean()`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p

            schema = p.boolean()
            ...

    Warning:
        When using the leaniant mode (see :func:`leaniant`), the regular expressions are
        case-insensitive. This means that you only need to handle lowercase variations of your
        regex. This also means that the regex can only handle case-insensitive cases.

    Inheritance:
        .. inheritance-diagram:: parasite.boolean.Boolean
            :parts: 1
    """

    _f_optional: bool = False  # Whether the value is optional.
    _f_nullable: bool = False  # Whether the value can be None.
    _f_leaniant: bool = False  # Whether the value is leaniant.

    _m_leaniant: tuple[str, str] = (
        r"^(true|1|yes|y)$",
        r"^(false|0|no|n)$",
    )  # The regular expressions for the true and false value.
    _m_literal: bool | None = None  # The literal value of the boolean.

    def __init__(self) -> None:
        pass

    def optional(self) -> Boolean:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Returns:
            Boolean: The updated instance of the class.

        Example usage::

            from parasite import p

            schema = p.obj({"name": p.boolean()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({})  # -> ValidationError: key "name" not found, but is required

            schema = p.obj({"name": p.boolean().optional()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({})  # -> { }
        """
        self._f_optional = True
        return self

    def required(self) -> Boolean:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Returns:
            Boolean: The updated instance of the class.

        Example usage::

            from parasite import p

            schema = p.obj({"name": p.boolean()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({})  # -> ValidationError: key "name" not found, but is required

            schema = p.obj({"name": p.boolean().required()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({})  # -> ValidationError: key "name" not found, but is required
        """
        self._f_optional = False
        return self

    def nullable(self) -> Boolean:
        """
        Set the value to be nullable.

        Returns:
            Boolean: The updated instance of the class.

        Example usage::

            from parasite import p

            schema = p.obj({"name": p.boolean()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({"name": None})  # -> ValidationError: key "name" cannot be None

            schema = p.obj({"name": p.boolean().nullable()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({"name": None})  # -> { "name": None }
        """
        self._f_nullable = True
        return self

    def not_nullable(self) -> Boolean:
        """
        Set the value to be not nullable.

        Returns:
            Boolean: The updated instance of the class.

        Example usage::

            from parasite import p

            schema = p.obj({"name": p.boolean()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({"name": None})  # -> ValidationError: key "name" cannot be None

            schema = p.obj({"name": p.boolean().not_nullable()})
            schema.parse({"name": True})  # -> { "name": True }
            schema.parse({"name": None})  # -> ValidationError: key "name" cannot be None
        """
        self._f_nullable = False
        return self

    def literal(self, value: bool) -> Boolean:
        """
        Set the literal value of the boolean.

        Args:
            value (bool): The literal value of the boolean.

        Returns:
            Boolean: The updated instance of the class.

        Example usage::

            from parasite import p

            schema = p.boolean()
            schema.parse(True)  # -> True
            schema.parse(False)  # -> False

            schema = p.boolean().literal(True)
            schema.parse(True)  # -> True
            schema.parse(False)  # -> ValidationError: object has to be True, but is False
        """
        self._m_literal = value
        return self

    def leaniant(self, re_true: Optional[str] = None, re_false: Optional[str] = None) -> Boolean:
        """
        Set the value to be leaniant. This allows the value to be read from a string or a number. As
        numbers only ``0`` (converts to: ``False``) and ``1`` (converts to: ``True``) are accepted.

        Note:
            All string input in leaniant mode is converted to lowercase before, so you only need to
            handle lowercase variations of your regex. By default the following regular expressions
            are used::

                re_true = r"^(true|1|yes|y)$"
                re_false = r"^(false|0|no|n)$"

        Args:
            re_true (Optional[str]): The regular expression for the true value. Default: None
            re_false (Optional[str]): The regular expression for the false value. Default: None

        Returns:
            Boolean: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.boolean().leaniant()
                schema2 = p.boolean()

            The resulting schemas will parse the following objects::

                >>> schema.parse(True)
                True
                >>> schema.parse("true")
                True
                >>> schema.parse("false")
                False
                >>> schema.parse(1)
                True

                >>> schema2.parse(True)
                True
                >>> schema2.parse("true")
                ValidationError: object has to be a boolean, but is 'true'
                >>> schema2.parse(1)
                ValidationError: object has to be a boolean, but is '1'
        """
        self._f_leaniant = True

        if re_true is not None:
            self._m_leaniant = (re_true, self._m_leaniant[1])

        if re_false is not None:
            self._m_leaniant = (self._m_leaniant[0], re_false)

        return self

    def parse(self, obj: Any) -> bool:
        # if obj is already a boolean, return it
        if isinstance(obj, bool):
            pass

        # if obj is a string and leaniant mode is active, try to convert it to a boolean
        elif isinstance(obj, str) and self._f_leaniant:
            # if obj is a string, try to convert it to a boolean
            if re.match(self._m_leaniant[0], obj.lower()):
                obj = True

            elif re.match(self._m_leaniant[1], obj.lower()):
                obj = False

            else:
                # raise an error if the value could not be matched to any regex
                raise ValidationError(
                    f"object has to be regex (true: {self._m_leaniant[0]!r}, false: "
                    f"{self._m_leaniant[1]!r}) accepted boolean value, but is {obj!r}"
                )

        # if obj is a number, try to convert it to a boolean
        elif isinstance(obj, (int, float)) and self._f_leaniant:
            # first check if the number is an actual number
            if math.isnan(obj):
                obj = False

            elif int(obj) == 1:
                obj = True

            elif int(obj) == 0:
                obj = False

            else:
                raise ValidationError(f"object has to be 1 or 0, but is {obj!r}")

        else:
            # raise an error if the value could not be parsed
            raise ValidationError(f"object has to be a boolean, but is {obj!r}")

        # if literal is set, check if obj is the literal value
        if self._m_literal is not None and obj != self._m_literal:
            raise ValidationError(f"object has to be {self._m_literal}, but is {obj}")

        return obj

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[bool | None]:
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            # if key is found, just package ``parse(..)`` it into a Some
            if value is not None:
                return Some(self.parse(value))

            # if value is None, check if the value is nullable
            if self._f_nullable:
                return Some(None)

            raise ValidationError(f"key {key!r} is not nullable, but is None")

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key {key!r} not found, but is required")
