try:
    set()
except:
    from sets import Set as set

__all__ = ('Register', 'testing')


class TestedDesc(object):
    def __get__(self, obj, typ=None):
        tested = list(typ._tested)
        tested.sort()
        return tested

class Register(object):
    _tested = set()
    
    def add(cls, test_obj):
        cls._tested.add(test_obj)
    add = classmethod(add)

    tested = TestedDesc()
        

def testing(*args):
    for arg in args:
        if type(arg) == str:
            Register.add(arg)
            continue
        module = arg.__module__
        try:
            klass = arg.im_class.__name__
            Register.add('%s.%s.%s' %(module, klass, arg.__name__))
        except AttributeError:
            Register.add('%s.%s' %(module, arg.__name__))
