####################
``parasite.variant``
####################

Brief
=====

Reference for the ``variant`` submodule of the ``parasite`` package. This submodule
contains the :class:`Variant` class, which is a generic container for a union of various Python
objects.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.variant([
      p.string(),
      p.number().integer(),
   ])

   schema.parse("42")  # -> "42"
   schema.parse(42)  # -> 42
   ...

Member Reference
================

.. automodule:: parasite.variant
   :members:
   :inherited-members:
   :undoc-members:

