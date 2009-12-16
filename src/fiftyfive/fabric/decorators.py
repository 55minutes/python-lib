def command(func):
    """
    A Fabric command decorator which registers it as a valid command.
    Uses the __all__ Python facility within a module.
    Make sure to declare `__all__ = []` at the top of your source code.
    """
    global __all__
    __all__.append(func.__name__)
    return func
