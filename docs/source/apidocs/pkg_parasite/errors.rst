###################
``parasite.errors``
###################

Brief
=====

This submodule contains the custom exceptions used by the parasite package.

Usage
=====

The exceptions are used to signal errors in the code. They are raised when the code encounters an
error that it cannot handle. The exceptions are used to provide a detailed error message to the
user.

.. code-block:: python

    from parasite import errors

    try:
        # code that may raise an exception
    except errors.ValidationError as e:
        print(e)

Member Reference
================

.. automodule:: parasite.errors
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance: