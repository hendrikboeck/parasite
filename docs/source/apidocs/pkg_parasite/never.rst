##################
``parasite.never``
##################

Brief
=====

Reference for the ``never`` submodule of the ``parasite`` package. This submodule
contains the :class:`Never` class, which is a simple class that always raises a
:class:`ValidationError` when called.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.never()
   schema.parse(1)  # ValidationError: this type can never be parsed
   ...

   schema = p.obj({ "name": p.never() })
   schema.parse({ "name": "John" })  # ValidationError: key 'name' found, but this type can never be parsed
   ...

Member Reference
================

.. automodule:: parasite.never
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:

