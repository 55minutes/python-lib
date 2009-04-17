"""
USA-specific Form helpers
"""

from itertools import chain

from django.forms.fields import Select

class USStateSelect(Select):
    """
    A Select widget that uses a list of U.S. states/territories as its choices.
    With the blank choice!
    """
    def __init__(self, attrs=None, render_empty=False, empty_label=u"---------"):
        from django.contrib.localflavor.us.us_states import STATE_CHOICES
        if render_empty:
            STATE_CHOICES = chain([('', empty_label or '')], STATE_CHOICES)
        super(USStateSelect, self).__init__(attrs, choices=STATE_CHOICES)
