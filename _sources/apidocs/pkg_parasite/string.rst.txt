###################
``parasite.string``
###################

Brief
=====

Reference for the ``string`` submodule of the ``parasite`` package. This submodule
contains the :class:`parasite.string.String` class, which is a generic container for a string
Python object.

Usage
=====

.. code-block:: python

   from parasite import p

   schema = p.string().min(3).max(10)

   schema.parse("hello")  # -> "hello"
   ...

Member Reference
================

.. automodule:: parasite.string
   :members:
   :inherited-members:
   :undoc-members:

