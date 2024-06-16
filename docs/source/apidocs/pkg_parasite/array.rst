##################
``parasite.array``
##################

Brief
=====

Reference for the ``array`` submodule of the ``parasite`` package. This submodule
contains the :class:`parasite.array.Array` class, which is a generic container for
a list of elements of a specific type.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.array()
   schema.parse([1])  # 1
   schema.parse(['hello'])  # 'hello'
   ...

   schema = p.array(p.number().integer())
   schema.parse([1, 2, 3])  # [1, 2, 3]
   schema.parse(["hello", "world"])  # ValidationError: Expected an integer, got 'hello'
   ...


Member Reference
================

.. automodule:: parasite.array
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance: