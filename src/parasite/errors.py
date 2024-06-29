class ValidationError(Exception):
    """
    Validation error that is raised when a value does not match the expected type.

    Inheritance:
        .. inheritance-diagram:: parasite.errors.ValidationError
            :parts: 1

    Example usage:
        Let's assume we have the following schema::

            from parasite import p

            schema = p.obj(
                {
                    "name": p.string().required(),
                    "age": p.number().integer().min(0).optional(),
                }
            )

        The schema will parse the following objects::

            from parasite import errors

            try:
                schema.parse({})

            except errors.ValidationError as e:
                print(e)
                # key "name" not found, but is required
    """
