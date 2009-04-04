import cgi, coverage, os, time

from templates import default_module_detail as module_detail
from templates import default_module_index as module_index

try:
    set
except:
    from sets import Set as set

__all__ = ('html_report','html_module_report')

class ModuleVars(object):
    modules = dict()
    def __new__(cls, *args, **kwargs):
        module = args[0]
        if cls.modules.get(module.__name__, None):
            return cls.modules.get(module.__name__)
        else:
            obj=super(ModuleVars, cls).__new__(cls)
            obj._init(module)
            cls.modules[module.__name__] = obj
            return obj

    def _init(self, module):
        module_name = module.__name__
        source_file, stmts, excluded, missing, missing_display = coverage.analysis2(module)
        executed = list(set(stmts).difference(missing))
        total = list(set(stmts).union(excluded))
        total.sort()
        title = module.__name__
        total_count = len(total)
        executed_count = len(executed)
        excluded_count = len(excluded)
        percent_covered = float(len(executed))/len(stmts)*100
        test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')

        for k, v in locals().iteritems():
            setattr(self, k, v)

    def as_dict(self):
        return self.__dict__

def html_report(modules, outdir):
    """
    TOP
    
    CONTENT_HEADER
    test_timestamp %s
    
    CONTENT_BODY
    module_stats %s
    total_lines %d
    total_executed %d
    total_excluded %d
    overall_covered %0.1f

    BOTTOM

    MODULE_STAT
    severity %s
    module_link %s
    module_name %s
    total_count %d
    executed_count %d
    excluded_count %d
    percent_covered %0.1f

    severity
    ========
    normal, warning, critical
    """
    outdir = os.path.abspath(outdir)
    modules = list(modules)
    modules.sort(key=lambda x: x.__name__)

    test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')

    m_subdirname = 'modules'
    m_dir = os.path.join(outdir, m_subdirname)
    try:
        os.mkdir(m_dir)
    except OSError:
        pass

    total_lines = 0
    total_executed = 0
    total_excluded = 0
    total_stmts = 0
    module_stats = list()
    for module in modules:
        m_vars = ModuleVars(module)
        m_vars.module_link = os.path.join(m_subdirname, m_vars.module_name + '.html')
        m_vars.severity = 'normal'
        if m_vars.percent_covered < 75: m_vars.severity = 'warning'
        if m_vars.percent_covered < 50: m_vars.severity = 'critical'
        module_stats.append(module_index.MODULE_STAT %m_vars.as_dict())
        total_lines += m_vars.total_count
        total_executed += m_vars.executed_count
        total_excluded += m_vars.excluded_count
        total_stmts += len(m_vars.stmts)
    module_stats = os.linesep.join(module_stats)
    overall_covered = float(total_executed)/total_stmts*100

    for i, module in enumerate(modules):
        m_vars = ModuleVars(module)
        nav = dict(up_link=os.path.join('..', 'index.html'),
                   up_label='index')
        if i != 0:
            m = ModuleVars(modules[i-1])
            nav['prev_link'] = os.path.basename(m.module_link)
            nav['prev_label'] = m.module_name
        if i+1 != len(modules):
            m = ModuleVars(modules[i+1])
            nav['next_link'] = os.path.basename(m.module_link)
            nav['next_label'] = m.module_name
        html_module_report(
            module, os.path.join(m_dir, m_vars.module_name + '.html'), nav)

    fo = file(os.path.join(outdir, 'index.html'), 'wb+')
    print >>fo, module_index.TOP
    print >>fo, module_index.CONTENT_HEADER %vars()
    print >>fo, module_index.CONTENT_BODY %vars()
    print >>fo, module_index.BOTTOM
    fo.close()

def html_module_report(module, filename, nav=None):
    """
    TOP
    title %s
    
    CONTENT_HEADER
    title %s
    source_file %s
    total_count %d
    executed_count %d
    excluded_count %d
    percent_covered %0.1f
    test_timestamp %s

    
    CONTENT_BODY
    source_lines %s

    BOTTOM

    SOURCE_LINE
    line_status %s
    source_line %s

    line_status
    ===========
    normal, executed, missed, excluded
    """
    if not nav:
        nav = {}
    m_vars = ModuleVars(module)

    m_vars.source_lines = source_lines = list()
    for i, source_line in enumerate(
        l.rstrip() for l in file(m_vars.source_file, 'rb').readlines()):
        line_status = 'normal'
        if i+1 in m_vars.executed: line_status = 'executed'
        if i+1 in m_vars.excluded: line_status = 'excluded'
        if i+1 in m_vars.missing: line_status = 'missed'
        source_lines.append(module_detail.SOURCE_LINE %vars())
    m_vars.source_lines = os.linesep.join(source_lines)

    if 'prev_link' in nav and 'next_link' in nav:
        nav_html = module_detail.NAV %nav
    elif 'prev_link' in nav:
        nav_html = module_detail.NAV_NO_NEXT %nav
    elif 'next_link' in nav:
        nav_html = module_detail.NAV_NO_PREV %nav
            
    fo = file(filename, 'wb+')
    print >>fo, module_detail.TOP %m_vars.as_dict()
    if nav:
        print >>fo, nav_html
    print >>fo, module_detail.CONTENT_HEADER %m_vars.as_dict()
    print >>fo, module_detail.CONTENT_BODY %m_vars.as_dict()
    if nav:
        print >>fo, nav_html
    print >>fo, module_detail.BOTTOM
    fo.close()
