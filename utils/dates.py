"Commonly-used date structures"

from django.utils.translation import ugettext_lazy as _

MONTHS = {
    1:_('Jan (01)'), 2:_('Feb (02)'), 3:_('Mar (03)'), 4:_('Apr (04)'),
    5:_('May (05)'), 6:_('Jun (06)'), 7:_('Jul (07)'), 8:_('Aug (08)'),
    9:_('Sep (09)'), 10:_('Oct (10)'), 11:_('Nov (11)'), 12:_('Dec (12)')
}

MONTHS_LONG = {
    1:_('January'), 2:_('February'), 3:_('March'), 4:_('April'),
    5:_('May'), 6:_('June'), 7:_('July'), 8:_('August'),
    9:_('September'), 10:_('October'), 11:_('November'), 12:_('December')
}
