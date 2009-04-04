import cgi, coverage, os

from html_template import *

try:
    set
except:
    from sets import Set as set

__all__ = ('output_module_html',)

def output_module_html(module, outdir):
    src_file, stmts, excluded, missing, missing_display = coverage.analysis2(module)
    if not missing:
        return
    executed = list(set(stmts).difference(missing))
    total = list(set(stmts).union(excluded))
    total.sort()
    fo = file(os.path.join(outdir, module.__name__ + '.html'), 'w+')
    print >>fo, HTML_TOP %module.__name__
    print >>fo, "<h1><code>%s</code></h1>" %module.__name__
    print >>fo, "<p>Source file: <b>%s</b></p>" %src_file
    print >>fo, "<p>file stats: <b>%d lines, %d excluded, %d executed: %0.1f%% covered</b></p>" \
          %(len(total), len(excluded), len(executed), float(len(executed))/len(stmts)*100)
    print >>fo, "<ol>"
    for i, l in enumerate(l.rstrip() for l in open(src_file, 'rb').readlines()):
        color = 'gray'
        if i+1 in executed: color="green"
        if i+1 in excluded: color="blue"
        if i+1 in missing: color="red"
        print >>fo, '<li style="color:%s"><code>%s</code></li>' %(color, cgi.escape(l))
    print >>fo, "</ol>"
    print >>fo, HTML_BOTTOM
    fo.close()
