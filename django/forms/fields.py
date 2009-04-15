import datetime

from django.forms import DateField, ValidationError
from django.utils.translation import ugettext_lazy as _

__all__ = ('LaterOrEqualDateField',)

class LaterOrEqualDateField(DateField):
    """
    A datefield in which the user entered value must be later than or
    equal to the specified ``min_date`` (defaults to
    ``datetime.date.today()``).
    Optionally specify whether the ``min_date`` should be updated at runtime
    with ``datetime.timedelta`` of current date and instantiation date
    (defaults to ``True``).
    """
    default_error_messages = {
        'min_date': _(u'Enter a date on or after %(min_date)s.'),
    }
    
    def __init__(self, min_date=None, runtime_update=True, *args, **kwargs):
        self.instantiated = datetime.date.today()
        if min_date is None:
            min_date = datetime.date.today()
        if not isinstance(min_date, datetime.date):
            raise TypeError("min_date must be a datetime.date object.")
        self.min_date = min_date
        self.runtime_update = bool(runtime_update)
        super(LaterOrEqualDateField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates that the input is later than or equal to the date
        specified by min_date. Returns a Python datetime.date object.
        """
        value = super(LaterOrEqualDateField, self).clean(value)
        min_date = self.min_date
        if self.runtime_update:
            min_date += datetime.date.today() - self.instantiated
        if min_date > value:
            raise ValidationError(self.error_messages['min_date'] %vars())
        return value
