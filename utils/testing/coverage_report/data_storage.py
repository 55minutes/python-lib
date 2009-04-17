import coverage, time

try:
    set
except:
    from sets import Set as set


class ModuleVars(object):
    modules = dict()
    def __new__(cls, module_name, module=None):
        if cls.modules.get(module_name, None):
            return cls.modules.get(module_name)
        else:
            obj=super(ModuleVars, cls).__new__(cls)
            obj._init(module_name, module)
            cls.modules[module_name] = obj
            return obj

    def _init(self, module_name, module):
        source_file, stmts, excluded, missed, missed_display = coverage.analysis2(module)
        executed = list(set(stmts).difference(missed))
        total = list(set(stmts).union(excluded))
        total.sort()
        title = module.__name__
        total_count = len(total)
        executed_count = len(executed)
        excluded_count = len(excluded)
        missed_count = len(missed)
        try:
            percent_covered = float(len(executed))/len(stmts)*100
        except ZeroDivisionError:
            percent_covered = 100
        test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')
        severity = 'normal'
        if percent_covered < 75: severity = 'warning'
        if percent_covered < 50: severity = 'critical'

        for k, v in locals().iteritems():
            setattr(self, k, v)
