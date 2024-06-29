# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
import copy
from dataclasses import dataclass, field
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
    ``parasite`` type for creating and parsing dictionary based schemas. Will return a python
    ``dict[Any, Any]`` with the parsed values on success.

    Note:
        Please use ``p.obj(...)`` instead of instantiating this class directly. ``p`` can be
        imported with::

            from parasite import p

            schema = p.obj({...})
            ...

    Note:
        Calling the constructor with a dictionary of keys and their respective schemas will create a
        new schema. This is equivalent to calling :func:`add_item` for each key and schema. If no or
        an empty dictionary is passed, the schema will accept any kind of dictionary.

    Inheritance:
        .. inheritance-diagram:: parasite.object.Object
            :parts: 1
    """

    # The items of the dictionary schema.
    _m_items: dict[Any, ParasiteType] = field(default_factory=lambda: {})

    _f_optional: bool = False  # Whether the value is optional.
    _f_nullable: bool = False  # Whether the value can be None.
    # Whether the dictionary should be parsed and not allow any other keys to exist.
    _f_strict: bool = False
    # Whether the dictionary should be stripped of all keys that are not in the dictionary.
    _f_strip: bool = False

    def __init__(self, items: dict[Any, ParasiteType] = {}) -> None:
        """
        Args:
            items (dict[K, ParasiteType]): The schema of subitems of the dictionary. Default: {}.

        Example usage:
            You can create a dictionary schema by passing a dictionary of keys and their respective
            schemas. The following example shows how to create a schema for a dictionary with a
            the keys "name","age"::

                from parasite import p

                schema = p.obj({
                    "name": p.string(),
                    "age": p.number().integer().optional(),
                })
                schema2 = p.obj()

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": "John" })
                { "name": "John" }
                >>> schema.parse({ })
                ValidationError: key "name" not found, but is required

                >>> schema2.parse({ })
                { }
                >>> schema2.parse({ "name": "John" })
                { "name": "John" }
        """
        self._m_items = items

    def optional(self) -> Object:
        """
        Makes the value optional, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`required`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "sub": p.obj().optional() })
                schema2 = p.obj({ "sub": p.obj() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": { } })
                { "sub": { } }
                >>> schema.parse({ })
                { }

                >>> schema2.parse({ "sub": { } })
                { "sub": { } }
                >>> schema2.parse({ })
                ValidationError: key "sub" not found, but is required
        """
        self._f_optional = True
        return self

    def required(self) -> Object:
        """
        Makes the value required, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`optional`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`optional` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "sub": p.obj().optional().required() })
                schema2 = p.obj({ "sub": p.obj() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": { } })
                { "sub": { } }
                >>> schema.parse({ })
                ValidationError: key "sub" not found, but is required

                >>> schema2.parse({ "sub": { } })
                { "sub": { } }
                >>> schema2.parse({ })
                ValidationError: key "sub" not found, but is required
        """
        self._f_optional = False
        return self

    def nullable(self) -> Object:
        """
        Makes the value nullable, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`not_nullable`.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "sub": p.obj().nullable() })
                schema2 = p.obj({ "sub": p.obj() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": { } })
                { "sub": { } }
                >>> schema.parse({ "sub": None })
                { "sub": None }

                >>> schema2.parse({ "sub": { } })
                { "sub": { } }
                >>> schema2.parse({ "sub": None })
                ValidationError: key "sub" is not nullable, but is None
        """
        self._f_nullable = True
        return self

    def not_nullable(self) -> Object:
        """
        Makes the value not-nullable, when parsing with :func:`_find_and_parse`. Has no effect on
        :func:`parse`. Inverse of :func:`nullable`. Default behavior.

        Note:
            This function is default behavior for the class and therefore only has an effect if the
            function :func:`nullable` may have been called before.

        Warning:
            This function has no effect if the value is parsed as a standalone value.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "sub": p.obj().nullable().not_nullable() })
                schema2 = p.obj({ "sub": p.obj() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "sub": { } })
                { "sub": { } }
                >>> schema.parse({ "sub": None })
                ValidationError: key "sub" is not nullable, but is None

                >>> schema2.parse({ "sub": { } })
                { "sub": { } }
                >>> schema2.parse({ "sub": None })
                ValidationError: key "sub" is not nullable, but is None
        """
        self._f_nullable = False
        return self

    def strict(self) -> Object:
        """
        Set the dictionary to be strict. This function ensures that only the keys in the schema are
        allowed in the dictionary. If this function is used :func:`strip` has no effect.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.string() }).strict()
                schema2 = p.obj({ "name": p.string() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": "John" })
                { "name": "John" }
                >>> schema.parse({ "name": "John", "age": 20 })
                ValidationError: object has the key "age", but is not allowed to

                >>> schema2.parse({ "name": "John" })
                { "name": "John" }
                >>> schema2.parse({ "name": "John", "age": 20 })
                { "name": "John", "age": 20 }
        """
        self._f_strict = True
        return self

    def strip(self) -> Object:
        """
        Set the dictionary to be stripped. This will remove all keys that are not in the schema. In
        constrast to :func:`strict` this function does not raise an error if a key is not in the
        schema.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schemas::

                from parasite import p

                schema = p.obj({ "name": p.string() }).strip()
                schema2 = p.obj({ "name": p.string() })

            The resulting schemas will parse the following objects::

                >>> schema.parse({ "name": "John" })
                { "name": "John" }
                >>> schema.parse({ "name": "John", "age": 20 })
                { "name": "John" }

                >>> schema2.parse({ "name": "John" })
                { "name": "John" }
                >>> schema2.parse({ "name": "John", "age": 20 })
                { "name": "John", "age": 20 }
        """
        self._f_strip = True
        return self

    def extend(self, other: Object) -> Object:
        """
        Extend the dictionary with another dictionary. This will overwrite all values of the current
        dictionary with the values of the other dictionary if the key exists in both dictionaries.
        If you want to merge the dictionaries, use :func:`merge`.

        Args:
            other (Object): The dictionary to extend with.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following two schemas::

                from parasite import p

                schema = p.obj({ "name": p.string(), "age": p.string() })
                schema2 = p.obj({ "age": p.number().integer() })

            If we extend the two schemas, the resulting schema will be::

                # -> schema.extend(schema2)

                p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                })

            The resulting schema will parse the following objects::

                >>> schema.parse({ "name": "John", "age": 20 })
                { "name": "John", "age": 20 }

                >>> schema.parse({ "name": "John", "age": "20" })
                ValidationError: key "age" has to be an integer, but is 20
        """
        if not isinstance(other, Object):
            raise ValidationError(f"object has to be a dictionary, but is '{other!r}'")

        self._m_items.update(other._m_items)
        return self

    def merge(self, other: Object) -> Object:
        """
        Merge the dictionary with another dictionary. This tries to merge the values of the current
        dictionary with the values of the other dictionary. If the key exists in both dictionaries
        the value of the current dictionary will not be overwritten, but the values will be merged.
        This results in the following behavior:

        - If both values are objects, they will be merged into a single dictionary with :func:`merge`.
        - If both values are variants, they will be merged into a single variant.
        - If one value is a variant and the other is not, the value will be added to the variant.
        - If both values are something else, they will be merged into a new variant.

        Args:
            other (Object): The dictionary to merge with.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following two schemas::

                from parasite import p

                schema = p.obj({ "name": p.string(), "age": p.string() })
                schema2 = p.obj({ "age": p.number().integer() })

            If we merge the two schemas, the resulting schema will be::

                # -> schema.merge(schema2)

                p.obj({
                    "name": p.string(),
                    "age": p.variant([
                        p.string(),
                        p.number().integer(),
                    ])
                })

            The resulting schema will parse the following objects::

                >>> schema.parse({ "name": "John", "age": 20 })
                { "name": "John", "age": 20 }

                >>> schema.parse({ "name": "John", "age": "20" })
                { "name": "John", "age": "20" }
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
        Pick only the keys from the object. This will create a new :class:`Object` with only the
        keys found in the list. If a key is not found in the object, it will raise a KeyError. If
        you want to ignore keys that are not found, use :func:`pick_safe`.

        Args:
            keys (list[K]): The keys to pick.

        Returns:
            Object: New instance of the class with only the picked keys.

        Raises:
            KeyError: If a key is not found in the object.

        Example usage:
            Lets assume we have the following schema::

                from parasite import p

                schema = p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                    "city": p.string(),
                }).strict()

            If we pick the keys "name" and "age", the resulting schema will be::

                # -> schema = schema.pick(["name", "age"])

                p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                }).strict()

            The resulting schema will parse the following objects::

                >>> schema.parse({ "name": "John", "age": 20 })
                { "name": "John", "age": 20 }

                >>> schema.parse({ "name": "John", "age": 20, "city": "New York" })
                ValidationError: object has the key "city", but is not allowed to
        """
        new_obj = copy.deepcopy(self)
        new_obj._m_items = {key: self._m_items[key] for key in keys}
        return new_obj

    def pick_safe(self, keys: list) -> Object:
        """
        Pick only the keys from the object. This will create a new :class:`Object` with only the
        keys found in the list. If a key is not found in the object, it will be ignored. If you want
        to raise an error if a key is not found, use :func:`pick`.

        Args:
            keys (list[K]): The keys to pick.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schema::

                from parasite import p

                schema = p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                    "city": p.string(),
                }).strict()

            If we pick the keys "name" and "age", the resulting schema will be::

                # -> schema = schema.pick_safe(["name", "age"])

                p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                }).strict()

            The resulting schema will parse the following objects::

                >>> schema.parse({ "name": "John", "age": 20 })
                { "name": "John", "age": 20 }

                >>> schema.parse({ "name": "John", "age": 20, "city": "New York" })
                { "name": "John", "age": 20 }
        """
        new_obj = copy.deepcopy(self)
        new_obj._m_items = {key: self._m_items[key] for key in keys if key in self._m_items}
        return new_obj

    def omit(self, keys: list) -> Object:
        """
        Omit the keys from the object. This will create a new :class:`Object` with all keys except
        the ones found in the list.

        Args:
            keys (list[K]): The keys to omit.

        Returns:
            Object: New instance of the class with the omitted keys.

        Example usage:
            Lets assume we have the following schema::

                from parasite import p

                schema = p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                    "city": p.string(),
                }).strict()

            If we omit the keys "name" and "age", the resulting schema will be::

                # -> schema = schema.omit(["name", "age"])

                p.obj({
                    "city": p.string(),
                }).strict()

            The resulting schema will parse the following objects::

                >>> schema.parse({ "name": "John", "age": 20, "city": "New York" })
                ValidationError: object has the key "name", but is not allowed to

                >>> schema.parse({ "city": "New York" })
                { "city": "New York" }
        """
        new_obj = copy.deepcopy(self)
        new_obj._m_items = {key: value for key, value in self._m_items.items() if key not in keys}
        return new_obj

    def add_item(self, key: Any, item: ParasiteType) -> Object:
        """
        Add an item to the object. This will also overwrite the item if it already exists.

        Args:
            key (K): The key of the item.
            item (ParasiteType): The item to add.

        Returns:
            Object: The updated instance of the class.

        Example usage:
            Lets assume we have the following schema::

                from parasite import p

                schema = p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                }).strict()

            If we add the key "city" with a string schema, the resulting schema will be::

                # -> schema.add_item("city", p.string())

                p.obj({
                    "name": p.string(),
                    "age": p.number().integer(),
                    "city": p.string(),
                }).strict()

            The resulting schema will parse the following objects::

                >>> schema.parse({ "name": "John", "age": 20, "city": "New York" })
                { "name": "John", "age": 20, "city": "New York" }

                >>> schema.parse({ "name": "John", "age": 20 })
                ValidationError: key "city" not found, but is required
        """
        self._m_items[key] = item
        return self

    def parse(self, obj: Any) -> dict[Any, Any]:
        if not isinstance(obj, dict):
            raise ValidationError(f"object has to be a dictionary, but is {obj!r}")

        # If the dictionary should be strict, check if all keys are allowed.
        if self._f_strict:
            for key in obj.keys():
                if key not in self._m_items:
                    raise ValidationError(f"object has the key {key!r}, but is not allowed to")

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

            raise ValidationError(f"key {key!r} is not nullable, but is None")

        # If the value is optional, return a Nil.
        if self._f_optional:
            return Nil

        # If the value is required, raise an error.
        raise ValidationError(f"object has to be a dictionary, but is '{value!r}'")
