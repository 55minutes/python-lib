import calendar, datetime, re

from django import forms
from django.forms import widgets
from django.forms.extras import SelectDateWidget
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

from fiftyfive.utils.dates import MONTHS

__all__ = ('SelectMonthYearWidget', 'SpanHiddenInput', 'SpanWidget')


class SpanWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        if attrs:
            self.attrs.update(attrs)
        return mark_safe(u'<span%s>%s</span>' % (flatatt(self.attrs), value))


class SpanHiddenInput(forms.HiddenInput):
    def __init__(self, attrs=None, span_attrs=None):
        super(SpanHiddenInput, self).__init__(attrs)
        if span_attrs is None:
            self.span_attrs = dict()
        else:
            self.span_attrs = span_attrs

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        output = [mark_safe(u'<span%s>%s</span>' % (flatatt(self.span_attrs), value))]
        output.append(super(SpanHiddenInput, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class SelectMonthYearWidget(SelectDateWidget):
    """
    A Widget that splits date input into two <select> boxes for month and
    year only. The day will default to runtime's day, unless specified.
    To indicate last day of the month, input 31 or larger for ``day`` parameter.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """

    def __init__(self, attrs=None, months=None, years=None, day=None):
        """
        * months is an optional dictionary or list/tuple of tuples to use in the
        "month" select box. ``{1:'Jan', ...}`` or ``((1, 'Jan'), ...)``
        * years is an optional list/tuple of years to use in the "year" select box.
        * day is the day to be used to construct ``datetime.date`` value,
        if ``None``, runtime day will be used.
        """
        super(SelectMonthYearWidget, self).__init__(attrs, years)
        if months is None:
            months = MONTHS
        self.months = months
        if day is None:
            self.day = day
        else:
            self.day = int(day)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        if type(self.months) == dict:
            month_choices = self.months.items()
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        select_html = forms.Select(choices=month_choices).\
                      render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        local_attrs['id'] = self.year_field % id_
        select_html = forms.Select(choices=year_choices).\
                      render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def value_from_datadict(self, data, files, name):
        y, m = int(data.get(self.year_field % name)), int(data.get(self.month_field % name))
        if y and m:
            d = self.day
            if d is None:
                d = datetime.date.today().day
            days_in_month = calendar.monthrange(y, m)[1]
            if d > days_in_month: d = days_in_month
            return datetime.date(y, m, d)
        return data.get(name, None)
