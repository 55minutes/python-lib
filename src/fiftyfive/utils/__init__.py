from cookies import *
from querysets import *

class SimpleAttrs(object):
    """
    A convenience class that can be used to hold arbitrary attributes.
    For example, you can store your messages in your setting file,
    that way it's easy to change the messages as a simple configuration.

    Example::
        from fiftyfive.utils import SimpleAttrs

        class Messages(SimpleAttrs):
            pass
    
        REGISTRATION_MESSAGES = Messages(
        ADD_TO_CART = "%(course_name)s was added to your cart.",
        ADD_STUDENT = "%(student_name)s was added for %(course_name)s",
        ALREADY_IN_CART = "%(course_name)s is already in your cart.",
        )

    To override a specific message in your local settings, you can
    simply just override that specific message::
        REGISTRATION_MESSAGES.ADD_TO_CART = "You want to attend %(course_name)s."
    """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class DelayedAttrs(object):
    """
    A convenience class that can be used to hold arbitrary attributes.
    The twist is that the attributes are passed in as an initializing
    iterable and the entire iterable is then assigned to object
    attribute when the first time the object is queried for an anttribute.

    Example::
        from fiftyfive.utils import DelayedAttrs

        def _ledger_iter():
            for l in Ledger.objects.all():
                yield (l.slug, l)

        LEDGERS = DelayedAttrs(_ledger_iter())

    ``LEDGERS`` will merely hold onto ``_ledger_iter()`` until someone asks
    it for an attribute it doesn't know about. At that point it iterates through
    ``_ledger_iter()`` which returns a key value pair ``(k,v)`` and does
    ``setattr(self, k, v)``, then tries to return the value.
    """
    def __init__(self, attr_iter):
        if callable(attr_iter):
            self.attr_iter = attr_iter()
        else:
            self.attr_iter = attr_iter

    def __getattr__(self, name):
        for k, v in self.attr_iter:
            setattr(self, k, v)
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(
                "'%s' object has no attribute '%s'"\
                %(self.__class__.__name__, name)
                )
