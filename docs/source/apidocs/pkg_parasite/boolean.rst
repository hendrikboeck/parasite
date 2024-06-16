####################
``parasite.boolean``
####################

Brief
=====

Reference for the ``boolean`` submodule of the ``parasite`` package. This submodule
contains the :class:`parasite.any.Boolean` class, which is a generic container for
any Python object.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.boolean()
   schema.parse(True)  # True
   schema.parse(False)  # False
   schema.parse(1)  # ValidationError: Expected a boolean, got 1
   ...

   schema = p.boolean().leaniant()
   schema.parse(1)  # True
   schema.parse("true")  # True
   ...


Member Reference
================

.. automodule:: parasite.boolean
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance: