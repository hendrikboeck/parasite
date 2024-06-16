###################
``parasite.object``
###################

Brief
=====

Reference for the ``object`` submodule of the ``parasite`` package. This submodule
contains the :class:`Object` class, which is a generic container for a dictionary Python object.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.obj({
      "name": p.string(),
      "age": p.number().integer().min(0),
   }).strict()

   schema.parse({
      "name": "John",
      "age": 30,
   })  # -> {'name': 'John', 'age': 30 }
   ...

Member Reference
================

.. automodule:: parasite.object
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:

