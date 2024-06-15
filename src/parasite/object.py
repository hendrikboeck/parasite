# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from dataclasses import dataclass, field, replace
from typing import Any, TypeVar

# -- Library Imports --
from rusttypes.option import Nil, Option, Some

# -- Package Imports --
from parasite.errors import ValidationError
from parasite.type import ParasiteType, _NotFound
from parasite.variant import Variant

K = TypeVar("K")
"""Template type for the key in a dictionary."""


@dataclass
class Object(ParasiteType[dict[Any, Any]]):
    """
    Parasite type for representing dictionary values.

    Inheritance:
        ParasiteType[dict]

    Args:
        _f_optional (bool): Whether the value is optional. Default: False
        _f_nullable (bool): Whether the value can be None. Default: False
        _f_strict (bool): Whether the dictionary should be parsed and not allow any other keys to
        exist. Default: False
        _f_strip (bool): Whether the dictionary should be stripped of all keys that are not in the
        _m_items (dict[K, ParasiteType]): The items of the dictionary. Default: {}
    """
    # NOTE: do not move this attribute, this has to be first in the class, as it will break, reading
    # items from the dictionary functionality
    _m_items: dict[Any, ParasiteType] = field(default_factory = lambda: {})

    _f_optional: bool = False
    _f_nullable: bool = False
    _f_strict: bool = False
    _f_strip: bool = False

    def optional(self) -> Object:
        """
        Set the value to be optional.

        Returns:
            Object: The updated instance of the class.
        """
        self._f_optional = True
        return self

    def required(self) -> Object:
        """
        Set the value to be required.

        Returns:
            Object: The updated instance of the class.
        """
        self._f_optional = False
        return self

    def nullable(self) -> Object:
        """
        Set the value to be nullable.

        Returns:
            Object: The updated instance of the class.
        """
        self._f_nullable = True
        return self

    def non_nullable(self) -> Object:
        """
        Set the value to be non-nullable.

        Returns:
            Object: The updated instance of the class.
        """
        self._f_nullable = False
        return self

    def strict(self) -> Object:
        """
        Set the dictionary to be strict.

        Returns:
            Object: The updated instance of the class.
        """
        self._f_strict = True
        return self

    def strip(self) -> Object:
        """
        Set the dictionary to be stripped.

        Returns:
            Object: The updated instance of the class.
        """
        self._f_strip = True
        return self

    def extend(self, other: Object) -> Object:
        """
        Extend the dictionary with another dictionary.

        Args:
            other (Object): The dictionary to extend with.

        Returns:
            Object: The updated instance of the class.
        """
        if not isinstance(other, Object):
            raise ValidationError(f"object has to be a dictionary, but is '{other!r}'")

        self._m_items.update(other._m_items)
        return self

    def merge(self, other: Object) -> Object:
        """
        Merge the dictionary with another dictionary.

        Args:
            other (Object): The dictionary to merge with.

        Returns:
            Object: The updated instance of the class.
        """
        for key, value in other._m_items.items():

            # If the key is in the dictionary, merge the values.
            if key in self._m_items:
                # if both src and dest are objects, merge them
                if isinstance(value, Object) and isinstance(self._m_items[key], Object):
                    self._m_items[key].merge(value)

                # if both src and dest are arrays, merge them
                elif isinstance(value, Variant) and isinstance(self._m_items[key], Variant):
                    for variant in value._m_variants:
                        self._m_items[key].add_variant(variant)

                # if dest is already a variant, add the value to it
                elif isinstance(self._m_items[key], Variant):
                    self._m_items[key].add_variant(value)

                # else, create a new variant and add both values
                else:
                    org = self._m_items[key]
                    self._m_items[key] = Variant().add_variant(org).add_variant(value)

            # If the key is not in the dictionary, add it.
            else:
                self._m_items[key] = value

        return self

    def pick(self, keys: list) -> Object:
        """
        Pick only the keys from the dictionary.

        Args:
            keys (list[K]): The keys to pick.

        Returns:
            Object: New instance of the class with only the picked keys.
        """
        new_obj = replace(self)
        new_obj._m_items = {key: self._m_items[key] for key in keys}
        return new_obj

    def pick_safe(self, keys: list) -> Object:
        """
        Pick only the keys from the dictionary.

        Args:
            keys (list[K]): The keys to pick.

        Returns:
            Object: The updated instance of the class.
        """
        new_obj = replace(self)
        new_obj._m_items = {key: self._m_items[key] for key in keys if key in self._m_items}
        return new_obj

    def omit(self, keys: list) -> Object:
        """
        Omit the keys from the dictionary.

        Args:
            keys (list[K]): The keys to omit.

        Returns:
            Object: New instance of the class with the omitted keys.
        """
        new_obj = replace(self)
        new_obj._m_items = {key: value for key, value in self._m_items.items() if key not in keys}
        return new_obj

    def add_item(self, key: Any, item: ParasiteType) -> Object:
        """
        Add an item to the dictionary.

        Args:
            key (K): The key of the item.
            item (ParasiteType): The item to add.

        Returns:
            Object: The updated instance of the class.
        """
        self._m_items[key] = item
        return self

    def parse(self, obj: Any) -> dict[Any, Any]:
        if not isinstance(obj, dict):
            raise ValidationError(f"object has to be a dictionary, but is '{obj!r}'")

        # If the dictionary should be strict, check if all keys are allowed.
        if self._f_strict:
            for key in obj.keys():
                if key not in self._m_items:
                    raise ValidationError(f"object has the '{key}', but is not allowed to")

        # If the dictionary should be stripped, strip it.
        if self._f_strip:
            obj = {key: value for key, value in obj.items() if key in self._m_items.keys()}

        # Parse the dictionary.
        for key, item in self._m_items.items():
            item._find_and_parse(obj, key).map(lambda x: obj.update({key: x}))

        return obj

    def _find_and_parse(self, parent: dict[K, Any], key: K) -> Option[dict[K, Any] | None]:
        if (value := parent.get(key, _NotFound)) is not _NotFound:
            # If key is found, just package ``parse(..)`` it into a Some.
            if value is not None:
                return Some(self.parse(value))

            # If value is None, check if the value is nullable.
            if self._f_nullable:
                return Some(None)

        # If the value is optional, return a Nil.
        if self._f_optional:
            return Nil

        # If the value is required, raise an error.
        raise ValidationError(f"object has to be a dictionary, but is '{value!r}'")
