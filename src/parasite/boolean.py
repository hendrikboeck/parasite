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

    Inheritance:
        ParasiteType[bool]

    Args:
        _f_optional (bool): Whether the value is optional. Default: False
        _f_nullable (bool): Whether the value can be None. Default: False
        _m_leaniant (tuple[AnyStr, AnyStr]): The regular expressions for the true and false value.
        Default: (r"^(true|1|yes|y)$", r"^(false|0|no|n)$")
        _m_literal (bool | None): The literal value of the boolean. Default: None
    """
    _f_optional: bool = False
    _f_nullable: bool = False
    _f_leaniant: bool = False

    _m_leaniant: tuple[str, str] = (r"^(true|1|yes|y)$", r"^(false|0|no|n)$")
    _m_literal: bool | None = None

    def optional(self) -> Boolean:
        """
        Set the value to be optional.

        Returns:
            Boolean: The updated instance of the class.
        """
        self._f_optional = True
        return self

    def required(self) -> Boolean:
        """
        Set the value to be required.

        Returns:
            Boolean: The updated instance of the class.
        """
        self._f_optional = False
        return self

    def nullable(self) -> Boolean:
        """
        Set the value to be nullable.

        Returns:
            Boolean: The updated instance of the class.
        """
        self._f_nullable = True
        return self

    def non_nullable(self) -> Boolean:
        """
        Set the value to be not nullable.

        Returns:
            Boolean: The updated instance of the class.
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
        """
        self._m_literal = value
        return self

    def leaniant(self, re_true: Optional[str] = None, re_false: Optional[str] = None) -> Boolean:
        """
        Set the value to be leaniant.

        Args:
            re_true (Optional[str]): The regular expression for the true value. Default: None
            re_false (Optional[str]): The regular expression for the false value. Default: None

        Returns:
            Boolean: The updated instance of the class.
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
                    f"{self._m_leaniant[1]!r}) accepted boolean value, but is '{obj!r}'"
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
                raise ValidationError(f"object has to be 1 or 0, but is '{obj!r}'")

        else:
            # raise an error if the value could not be parsed
            raise ValidationError(f"object has to be a boolean, but is '{obj!r}'")

        # if literal is set, check if obj is the literal value
        if self._m_literal is not None and obj != self._m_literal:
            raise ValidationError(f"object has to be {self._m_literal}, but is {obj}")

        return obj

    def find_and_parse(self, parent: dict[K, Any], key: K) -> Option[bool | None]:
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
