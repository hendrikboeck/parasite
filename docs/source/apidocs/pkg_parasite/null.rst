#################
``parasite.null``
#################

Brief
=====

Reference for the ``null`` submodule of the ``parasite`` package. This submodule
contains the :class:`parasite.null.Null` class, which is a generic container for
a Python ``None`` object.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.null()
   schema.parse(None)  # -> None
   ...

Member Reference
================

.. automodule:: parasite.null
   :members:
   :inherited-members:
   :undoc-members:

