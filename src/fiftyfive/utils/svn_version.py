"""
Blatantly copied from django.utils.version
"""

import os.path
import re

def get_svn_revision(path):
    """
    Returns the SVN revision in the form XXXX,
    where XXXX is the revision number.

    Returns unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.
    """
    rev = None
    entries_path = '%s/.svn/entries' % path

    try:
        entries = open(entries_path, 'r').read()
    except IOError:
        pass
    else:
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match('(\d+)', entries):
            rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    if rev:
        return u'%s' % rev
    return u'unknown'
