# -- STL Imports --
from abc import ABC as _Namespace
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


class p(_Namespace):
    """
    sudo-namespace for all parasite types. Makes it easier to import and call them. Tries to mimic
    the behavior of the ``z`` object imported from ``zod`` library in JavaScript.

    Example::

        >>> from parasite import p
        >>>
        >>> schema = p.obj({
        ...     "name": p.string().required(),
        ...     "age": p.number().integer().min(0).optional(),
        ... }).strip()
        >>>
        >>> data = {
        ...     "name": "John Doe",
        ...     "age": 42,
        ...     "extra": "This will be stripped",
        ... }
        >>>
        >>> schema.parse(data)
        {'name': 'John Doe', 'age': 42}
        >>>
        >>> schema.parse({})
        ValidationError: Missing required key: 'name'
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
