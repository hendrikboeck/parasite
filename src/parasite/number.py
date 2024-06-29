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

Numerical = int | float


@dataclass
class Number(ParasiteType[Numerical]):
    """
    Parasite type for representing numerical values. This type can parse both integers and floats.

    Note:
        Please use ``p.number()`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p

            schema = p.number()
            ...
    """

    _f_optional: bool = False  # Wether the value is optional
    _f_nullable: bool = False  # Wether the value can be None
    _f_integer: bool = False  # Wether the value has to be an integer

    _f_lt: bool = False  # Wether the value has to be less than a certain value
    _f_lte: bool = False  # Wether the value has to be less than or equal to a certain value
    _f_gt: bool = False  # Wether the value has to be greater than a certain value
    _f_gte: bool = False  # Wether the value has to be greater than or equal to a certain value

    _m_ul: Numerical | None = None  # Upper limit for the value
    _m_ll: Numerical | None = None  # Lower limit for the value

    def __init__(self) -> None:
        pass

    def optional(self) -> Number:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Returns:
            Number: modified instance
        """
        self._f_optional = True
        return self

    def required(self) -> Number:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Returns:
            Number: modified instance
        """
        self._f_optional = False
        return self

    def nullable(self) -> Number:
        """
        Makes the value nullable, when parsing with ``_find_and_parse(..)``. Has no effect on
        ``parse(..)``. Inverse of ``not_nullable(..)``.

        Returns:
            Number: modified instance
        """
        self._f_nullable = True
        return self

    def not_nullable(self) -> Number:
        """
        Makes the value not-nullable, when parsing with ``_find_and_parse(..)``. Has no effect on
        ``parse(..)``. Default behavior. Inverse of ``nullable(..)``.

        Returns:
            Number: modified instance
        """
        self._f_nullable = False
        return self

    def integer(self) -> Number:
        """
        Makes the value an integer, when parsing with ``_find_and_parse(..)``. Has no effect on
        ``parse(..)``. Inverse of ``float(..)``.

        Returns:
            Number: modified instance
        """
        self._f_integer = True
        return self

    def float(self) -> Number:
        """
        Makes the value a float, when parsing with ``_find_and_parse(..)``. Has no effect on
        ``parse(..)``. Default behavior. Inverse of ``integer(..)``.

        Returns:
            Number: modified instance
        """
        self._f_integer = False
        return self

    def gt(self, value: Numerical) -> Number:
        """
        Sets the lower limit for the value. The value has to be greater than the specified value.

        Args:
            value (Numerical): lower limit for the value

        Returns:
            Number: modified instance
        """
        self._f_gte = False
        self._f_gt = True
        self._m_ll = value
        return self

    def gte(self, value: Numerical) -> Number:
        """
        Sets the lower limit for the value. The value has to be greater than or equal to the
        specified value.

        Args:
            value (Numerical): lower limit for the value

        Returns:
            Number: modified instance
        """
        self._f_gt = False
        self._f_gte = True
        self._m_ll = value
        return self

    def positive(self) -> Number:
        """
        Sets the lower limit for the value. The value has to be greater than 0.

        Returns:
            Number: modified instance
        """
        return self.gt(0)

    def not_negative(self) -> Number:
        """
        Sets the lower limit for the value. The value has to be greater than or equal to 0.

        Returns:
            Number: modified instance
        """
        return self.gte(0)

    def min(self, value: Numerical) -> Number:
        """
        Sets the lower limit for the value. The value has to be greater than or equal to the
        specified value.

        Args:
            value (Numerical): lower limit for the value

        Returns:
            Number: modified instance
        """
        return self.gte(value)

    def lt(self, value: Numerical) -> Number:
        """
        Sets the upper limit for the value. The value has to be less than the specified value.

        Args:
            value (Numerical): upper limit for the value

        Returns:
            Number: modified instance
        """
        self._f_lte = False
        self._f_lt = True
        self._m_ul = value
        return self

    def lte(self, value: Numerical) -> Number:
        """
        Sets the upper limit for the value. The value has to be less than or equal to the specified
        value.

        Args:
            value (Numerical): upper limit for the value

        Returns:
            Number: modified instance
        """
        self._f_lt = False
        self._f_lte = True
        self._m_ul = value
        return self

    def negative(self) -> Number:
        """
        Sets the upper limit for the value. The value has to be less than 0.

        Returns:
            Number: modified instance
        """
        return self.lt(0)

    def not_positive(self) -> Number:
        """
        Sets the upper limit for the value. The value has to be less than or equal to 0.

        Returns:
            Number: modified instance
        """
        return self.lte(0)

    def max(self, value: Numerical) -> Number:
        """
        Sets the upper limit for the value. The value has to be less than or equal to the specified
        value.

        Args:
            value (Numerical): upper limit for the value

        Returns:
            Number: modified instance
        """
        return self.lte(value)

    def _parse(self, obj: Numerical) -> Numerical:
        """
        Private function for parsing the value. This function is called by ``parse(..)`` and should
        not be called directly by the user.

        Throws:
            ValidationError: if the value could not be parsed or was invalid

        Args:
            obj (Numerical): value to parse

        Returns:
            Numerical: parsed destination value
        """
        # cast to integer, if required
        if self._f_integer:
            self._m_ll = int(self._m_ll) if self._m_ll is not None else None
            self._m_ul = int(self._m_ul) if self._m_ul is not None else None

        if self._f_lt and obj >= self._m_ul:
            raise ValidationError(f"object has to be < '{self._m_ul}', but is {obj!r}")

        elif self._f_lte and obj > self._m_ul:
            raise ValidationError(f"object has to be =<'{self._m_ul}', but is {obj!r}")

        if self._f_gt and obj <= self._m_ll:
            raise ValidationError(f"object has to be > '{self._m_ll}', but is {obj!r}")

        elif self._f_gte and obj < self._m_ll:
            raise ValidationError(f"object has to be >='{self._m_ll}', but is {obj!r}")

        return obj

    def parse(self, obj: Any) -> Numerical:
        # python handles bool as int, so we have to check for bool first
        if isinstance(obj, bool):
            # fallthrough on boolean values
            pass

        elif isinstance(obj, float):
            if self._f_integer:
                raise ValidationError(f"object has to be an integer, but is {obj!r}")
            return float(self._parse(obj))

        elif isinstance(obj, int):
            return int(self._parse(obj))

        raise ValidationError(f"object has to be a number, but is {obj!r}")

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[Numerical | None]:
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
