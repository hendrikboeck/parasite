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
    """sudo-namespace for all parasite types. Makes it easier to import and call them."""
    any: TypeAlias = Any_
    null: TypeAlias = Null
    number: TypeAlias = Number
    string: TypeAlias = String
    boolean: TypeAlias = Boolean
    never: TypeAlias = Never
    variant: TypeAlias = Variant
    obj: TypeAlias = Object
    array: TypeAlias = Array
