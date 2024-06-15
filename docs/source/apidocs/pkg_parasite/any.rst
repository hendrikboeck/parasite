###########################
``any`` Submodule Reference
###########################

Brief
=====

Reference for the ``any`` submodule of the ``parasite`` package. This submodule
contains the :class:`parasite.any.Any_` class, which is a generic container for
any Python object.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.any()
   schema.parse(1)  # 1
   schema.parse('hello')  # 'hello'
   ...

   schema = p.obj({ "payload": p.any().optional() })
   schema.parse({ "payload": 1 })  # { "payload": 1 }
   schema.parse({ })  # { }
   ...


Member Reference
================

.. automodule:: parasite.any
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance: