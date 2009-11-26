__all__ = ('attach_to_queryset_objects', )

def attach_to_queryset_objects(queryset, attrs):
    """
    Attaches extra attributes to each object in a Django ``Queryset``
    and returns the modified queryset.
    attrs are specified as a dictionary ``{'attr_name': attr_value}``,
    if ``attr_value`` is a callable, it must accept either a queryset.object
    as a parameter, or accept no parameters at all.
    """

    for obj in queryset:
        for name, value in attrs.iteritems():
            if callable(value):
                try:
                    value = value(obj)
                except TypeError:
                    value = value()
            setattr(obj, name, value)
    return queryset
