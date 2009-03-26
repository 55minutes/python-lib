"""
Context processor for lightweight session messages.
"""
from django.utils.encoding import StrAndUnicode

from message import get_and_delete_messages

def session_messages (request):
    """
    Returns session messages for the current session.
    """
    session_messages = dict()
    for category in request.session.get('messages', dict()).keys():
        session_messages[category] = LazyMessages(request.session, category)
    return dict(session_messages=session_messages)

class LazyMessages(StrAndUnicode):
    """
    Lazy message container, so messages aren't actually retrieved from
    session and deleted until the template asks for them.
    """
    def __init__(self, session, category='info'):
        self.session, self.category = session, category

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    def __nonzero__(self):
        return bool(self.messages)

    def __unicode__(self):
        return unicode(self.messages)

    def __getitem__(self, *args, **kwargs):
        return self.messages.__getitem__(*args, **kwargs)

    def _get_messages(self):
        if hasattr(self, '_messages'):
            return self._messages
        self._messages = get_and_delete_messages(self.session, self.category)
        return self._messages
    messages = property(_get_messages)
