# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass
from re import Pattern
import re
from typing import Any, TypeVar
from enum import Enum

# -- Library Imports --
from rusttypes.option import Nil, Option, Some
import tracing

# -- Package Imports --
from parasite import _const
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class String(ParasiteType[str]):
    """
    Parasite type for representing string values.

    Inheritance:
        ParasiteType[str]

    Args:
        _f_optional (bool): Whether the value is optional. Default: False
        _f_nullable (bool): Whether the value can be None. Default: False
        _f_transform_before_parse (bool): Whether to transform the value before parsing.
        Default: False
        _f_trim (bool): Whether to trim the value. Default: False
        _f_to_lower (bool): Whether to convert the value to lowercase. Default: False
        _f_to_upper (bool): Whether to convert the value to uppercase. Default: False
        _m_regex_t (_RegexType): Type of regex to use for validation. Default: NONE
        _m_ul (int | None): Upper limit for the value. Default: None
        _m_ll (int | None): Lower limit for the value. Default: None
        _m_starts (str | None): String that the value must start with. Default: None
        _m_ends (str | None): String that the value must end with. Default: None
        _m_contains (str | None): String that the value must contain. Default: None
        _m_regex (Pattern | None): Compiled regex pattern to use for validation, if _m_regex_t is
        REGEX. Default: None
    """

    class _RegexType(Enum):
        """
        Enum for the different types of regexes that can be used to validate a string.
        """
        NONE = 0
        EMAIL = 1
        URL = 2
        UUID = 3
        CUID = 4
        CUID2 = 5
        ULID = 6
        IPV4 = 7
        IPV6 = 8
        REGEX = 9

    # flags
    _f_optional: bool = False
    _f_nullable: bool = False
    _f_transform_before_parse: bool = False

    # transformation flags
    _f_trim: bool = False
    _f_to_lower: bool = False
    _f_to_upper: bool = False

    _m_regex_t: _RegexType = _RegexType.NONE
    _m_ul: int | None = None
    _m_ll: int | None = None

    _m_starts: str | None = None
    _m_ends: str | None = None
    _m_contains: str | None = None
    _m_regex: Pattern | None = None

    def optional(self) -> String:
        """
        Makes the value optional, when parsing with `find_and_parse(..)`. Has no effect on
        `parse(..)`. Inverse of `required(..)`.

        Returns:
            String: modified instance
        """
        self._f_optional = True
        return self

    def required(self) -> String:
        """
        Makes the value required, when parsing with `find_and_parse(..)`. Has no effect on
        `parse(..)`. Inverse of `optional(..)`. Default behavior.

        Returns:
            String: modified instance
        """
        self._f_optional = False
        return self

    def nullable(self) -> String:
        """
        Makes the value nullable, when parsing with `find_and_parse(..)`. Has no effect on
        `parse(..)`. Inverse of `non_nullable(..)`.

        Returns:
            String: modified instance
        """
        self._f_nullable = True
        return self

    def non_nullable(self) -> String:
        """
        Makes the value non-nullable, when parsing with `find_and_parse(..)`. Has no effect on
        `parse(..)`. Inverse of `nullable(..)`. Default behavior.

        Returns:
            String: modified instance
        """
        self._f_nullable = False
        return self

    def trim(self) -> String:
        """
        Trims the value.

        Returns:
            String: modified instance
        """
        self._f_trim = True
        return self

    def to_lower(self) -> String:
        """
        Converts the value to lowercase.

        Returns:
            String: modified instance
        """
        self._f_to_lower = True
        return self

    def to_upper(self) -> String:
        """
        Converts the value to uppercase.

        Returns:
            String: modified instance
        """
        self._f_to_upper = True
        return self

    def transform_before_parse(self) -> String:
        """
        Transforms the value before parsing.

        Returns:
            String: modified instance
        """
        self._f_transform_before_parse = True
        return self

    def min(self, value: int) -> String:
        """
        Sets the lower length limit for the string value.

        Args:
            value (int): lower limit

        Returns:
            String: modified instance
        """
        self._m_ll = value
        return self

    def max(self, value: int) -> String:
        """
        Sets the upper length limit for the string value.

        Args:
            value (int): upper limit

        Returns:
            String: modified instance
        """
        self._m_ul = value
        return self

    def length(self, value: int) -> String:
        """
        Sets the lower and upper limit for the value.

        Args:
            value (int): length of the value

        Returns:
            String: modified instance
        """
        self._m_ll = value
        self._m_ul = value
        return self

    def not_empty(self) -> String:
        """
        Sets the lower limit for the value. The value has to be non-empty.

        Returns:
            String: modified instance
        """
        return self.min(1)

    def starts_with(self, value: str) -> String:
        """
        Sets the value that the string must start with.

        Args:
            value (str): string that the value must start with

        Returns:
            String: modified instance
        """
        self._m_starts = value
        return self

    def ends_with(self, value: str) -> String:
        """
        Sets the value that the string must end with.

        Args:
            value (str): string that the value must end with

        Returns:
            String: modified instance
        """
        self._m_ends = value
        return self

    def contains(self, value: str) -> String:
        """
        Sets the value that the string must contain.

        Args:
            value (str): string that the value must contain

        Returns:
            String: modified instance
        """
        self._m_contains = value
        return self

    def email(self) -> String:
        """
        Sets the regex type to email.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.EMAIL
        return self

    def url(self) -> String:
        """
        Sets the regex type to URL.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.URL
        return self

    def uuid(self) -> String:
        """
        Sets the regex type to UUID.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.UUID
        return self

    def cuid(self) -> String:
        """
        Sets the regex type to CUID.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.CUID
        return self

    def cuid2(self) -> String:
        """
        Sets the regex type to CUID2.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.CUID2
        return self

    def ulid(self) -> String:
        """
        Sets the regex type to ULID.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.ULID
        return self

    def ipv4(self) -> String:
        """
        Sets the regex type to IPv4.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.IPV4
        return self

    def ipv6(self) -> String:
        """
        Sets the regex type to IPv6.

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.IPV6
        return self

    def regex(self, value: Pattern) -> String:
        """
        Sets the regex pattern to use for validation.

        Args:
            value (Pattern): compiled regex pattern

        Returns:
            String: modified instance
        """
        self._m_regex_t = self._RegexType.REGEX
        self._m_regex = value
        return self

    def match(self, value: str) -> String:
        """
        Sets the regex pattern to use for validation.

        Args:
            value (str): regex pattern

        Returns:
            String: modified instance
        """
        return self.regex(re.compile(value))

    def _apply_transformations(self, value: str) -> str:
        """
        Applies the transformations on the value.

        Args:
            value (str): value to transform

        Returns:
            str: transformed value
        """
        if self._f_trim:
            value = value.strip()

        if self._f_to_lower:
            value = value.lower()

        if self._f_to_upper:
            value = value.upper()

        return value

    def _parse_bounds(self, value: str) -> str:
        """
        Parses the value with the length _constraints.

        Args:
            value (str): value to parse

        Returns:
            str: parsed value
        """
        if self._m_ll is not None and len(value) < self._m_ll:
            raise ValidationError(f"length of value '{value}' is less than {self._m_ll}")

        if self._m_ul is not None and len(value) > self._m_ul:
            raise ValidationError(f"length of value '{value}' is greater than {self._m_ul}")

        return value

    def _parse_basic(self, value: str) -> str:
        """
        Parses the value with the basic _constraints.

        Args:
            value (str): value to parse

        Returns:
            str: parsed value
        """
        if self._m_starts is not None and not value.startswith(self._m_starts):
            raise ValidationError(f"value '{value}' does not start with '{self._m_starts}'")

        if self._m_ends is not None and not value.endswith(self._m_ends):
            raise ValidationError(f"value '{value}' does not end with '{self._m_ends}'")

        if self._m_contains is not None and self._m_contains not in value:
            raise ValidationError(f"value '{value}' does not contain '{self._m_contains}'")

        return value

    def _parse_regex(self, value: str) -> str:
        """
        Parses the value with the regex _constraints.

        Args:
            value (str): value to parse

        Returns:
            str: parsed value
        """
        match self._m_regex_t:
            case self._RegexType.NONE:
                return value

            case self._RegexType.EMAIL:
                r = re.match(_const.RE_EMAIL, value)
                print(f"r: {r!r}, regex = {_const.RE_EMAIL!r}")

                if not _const.RE_EMAIL.match(value):
                    raise ValidationError(f"value '{value}' is not a valid email")
                return value

            case self._RegexType.URL:
                if not _const.RE_URL.match(value):
                    raise ValidationError(f"value '{value}' is not a valid URL")
                return value

            case self._RegexType.UUID:
                if not _const.RE_UUID.match(value):
                    raise ValidationError(f"value '{value}' is not a valid UUID")
                return value

            case self._RegexType.CUID:
                if not _const.RE_CUID.match(value):
                    raise ValidationError(f"value '{value}' is not a valid CUID")
                return value

            case self._RegexType.CUID2:
                if not _const.RE_CUID2.match(value):
                    raise ValidationError(f"value '{value}' is not a valid CUID2")
                return value

            case self._RegexType.ULID:
                if not _const.RE_ULID.match(value):
                    raise ValidationError(f"value '{value}' is not a valid ULID")
                return value

            case self._RegexType.IPV4:
                if not _const.RE_IPV4.match(value):
                    raise ValidationError(f"value '{value}' is not a valid IPv4")
                return value

            case self._RegexType.IPV6:
                if not _const.RE_IPV6.match(value):
                    raise ValidationError(f"value '{value}' is not a valid IPv6")
                return value

            case self._RegexType.REGEX:
                if not self._m_regex:
                    raise ValidationError("no regex pattern provided")
                if not self._m_regex.match(value):
                    raise ValidationError(f"value '{value}' does not match the regex pattern")
                return value

            case _:
                pass

        tracing.warn(f"unsupported regex type {self._m_regex_t!r}")
        return value

    def parse(self, obj: Any) -> str:
        if not isinstance(obj, str):
            raise ValidationError(f"expected a string, but got '{obj!r}'")

        if self._f_transform_before_parse:
            obj = self._apply_transformations(obj)

        obj = self._parse_bounds(obj)
        obj = self._parse_basic(obj)
        obj = self._parse_regex(obj)

        if not self._f_transform_before_parse:
            obj = self._apply_transformations(obj)

        return obj

    def find_and_parse(self, parent: dict[K, Any], key: K) -> Option[str | None]:
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            if value is not None:
                # if key is found, just package `parse(..)` it into a Some
                return Some(self.parse(value))

            # if value is None, check if the value is nullable
            if self._f_nullable:
                return Some(None)

            raise ValidationError(f"key '{key}' cannot be None")

        # if key is not found, return Nil if optional, else raise an error
        if self._f_optional:
            return Nil

        raise ValidationError(f"key '{key}' not found, but is required")
