class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        if getattr(cls, '__instance__', None) is None:
            instance = cls.__new__(cls)
            instance.__init__(*args, **kwargs)
            cls.__instance__ = instance
        return cls.__instance__


class PluginMount(type):
    """
    This implementation references Marty Alchin's excellent `"Pro Django"
    <http://www.apress.com/book/view/9781430210474>`_.
    """
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)
