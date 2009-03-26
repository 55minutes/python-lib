from fiftyfive.utils import SimpleAttrs

__all__ = (
    'Messages', 'create_message', 'get_and_delete_messages',
    'create_form_error_messages',
    )

class Messages(SimpleAttrs):
    """
    An optional convenience class that can be used to hold messages.
    For example, you can store your messages in your setting file,
    that way it's easy to change the messages as a simple configuration.

    Example::
        from fiftyfive.utils.session_messages import Messages
    
        REGISTRATION_MESSAGES = Messages(
        ADD_TO_CART = "%(course_name)s was added to your cart.",
        ADD_STUDENT = "%(student_name)s was added for %(course_name)s",
        ALREADY_IN_CART = "%(course_name)s is already in your cart.",
        )

    To override a specific message in your local settings, you can
    simply just override that specific message::
        REGISTRATION_MESSAGES.ADD_TO_CART = "You want to attend %(course_name)s."
    """
    pass

def create_message(session, message, category='info'):
    """
    Create a message in the current session, in a specific category.
    """
    messages = session.setdefault('messages', dict())
    
    try:
        messages[category].append(message)
    except KeyError:
        messages[category] = [message]

def create_form_error_messages(session, form_errors, category='error'):
    form_errors = form_errors.copy()
    for error in form_errors.pop('__all__', list()):
        create_message(session, unicode(error), category=category)
    for field, errors in form_errors.iteritems():
        for error in errors: create_message(
            session, '%s: %s' %(field.capitalize(), unicode(error)),
            category=category
            )

def get_and_delete_messages(session, category='info'):
    """
    Get and delete all messages from specific category for current session.
    """
    session_messages = session.get('messages', dict())
    session.modified = True
    return session_messages.pop(category, list())
