# -- STL Imports --
from typing import TypeAlias

# -- Package Imports --
from parasite.any import Any_
from parasite.array import Array
from parasite.boolean import Boolean
from parasite.null import Null
from parasite.number import Number
from parasite.object import Object
from parasite.string import String
from parasite.variant import Variant
from parasite.never import Never


class Namespace():
    """Abstract base class for all namespace implementations. This class tries to mimic the behavior
    of a namespace in other programming languages.

    Warning:
        Do not instantiate this class directly. It is only meant to be used as a base class for
        namespace implementations.

    Inheritance:
        .. inheritance-diagram:: parasite.Namespace
            :parts: 1
    """

    def __init__(self) -> None:
        """
        Raises:
            TypeError: Always, as this class is not meant to be instantiated.
        """
        raise TypeError("cannot instantiate a namespace")


class p(Namespace):
    """
    sudo-namespace for all ``parasite`` types. Makes it easier to import and call them. Tries to
    mimic the behavior of the ``z`` object imported from ``zod`` library in JavaScript.

    Inheritance:
        .. inheritance-diagram:: parasite.p
            :parts: 1

    Raises:
        TypeError: Always, as this class is not meant to be instantiated.

    Example usage:
        Let's assume we have the following schema::

            from parasite import p

            schema = p.obj({
                "name": p.string().required(),
                "age": p.number().integer().min(0).optional(),
            }).strip()

        and the following data::

            data = {
                "name": "John Doe",
                "age": 42,
                "extra": "This will be stripped",
            }

        The schema will parse the following objects::

            >>> schema.parse(data)
            { "name": "John Doe", "age": 42 }

            >>> schema.parse({})
            ValidationError: key "name" not found, but is required
    """
    any: TypeAlias = Any_
    null: TypeAlias = Null
    number: TypeAlias = Number
    string: TypeAlias = String
    boolean: TypeAlias = Boolean
    never: TypeAlias = Never
    variant: TypeAlias = Variant
    obj: TypeAlias = Object
    array: TypeAlias = Array
