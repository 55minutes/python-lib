__all__ = ('Packages', 'Modules', 'Excluded', 'Errors')

class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        if getattr(cls, '__instance__', None) is None:
            instance = cls.__new__(cls)
            instance.__init__(*args, **kwargs)
            cls.__instance__ = instance
        return cls.__instance__

class Packages(object):
    __metaclass__ = SingletonType
    packages = {}

class Modules(object):
    __metaclass__ = SingletonType
    modules = {}

class Excluded(object):
    __metaclass__ = SingletonType
    excluded = []

class Errors(object):
    __metaclass__ = SingletonType
    errors = []
