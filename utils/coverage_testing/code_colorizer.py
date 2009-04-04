import cgi, coverage, os, time

from default_html_template import *

try:
    set
except:
    from sets import Set as set

__all__ = ('output_module_html',)

def output_module_html(module, outdir):
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
    line_style %s
    source_line %s

    normal, executed, missed, excluded
    """
    source_file, stmts, excluded, missing, missing_display = coverage.analysis2(module)
    if not missing:
        return
    executed = list(set(stmts).difference(missing))
    total = list(set(stmts).union(excluded))
    total.sort()
    fo = file(os.path.join(outdir, module.__name__ + '.html'), 'wb+')

    title = module.__name__
    total_count = len(total)
    executed_count = len(executed)
    excluded_count = len(excluded)
    percent_covered = float(len(executed))/len(stmts)*100
    test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')

    source_lines = list()
    for i, source_line in enumerate(
        l.rstrip() for l in open(source_file, 'rb').readlines()):
        line_style = 'normal'
        if i+1 in executed: line_style = 'executed'
        if i+1 in excluded: line_style = 'excluded'
        if i+1 in missing: line_style = 'missed'
        source_lines.append(SOURCE_LINE %vars())
    source_lines = os.linesep.join(source_lines)

    print >>fo, TOP %vars()
    print >>fo, CONTENT_HEADER %vars()
    print >>fo, CONTENT_BODY %vars()
    print >>fo, BOTTOM
    fo.close()
