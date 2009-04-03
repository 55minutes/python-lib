import cgi, coverage, os

try:
    set
except:
    from sets import Set as set

def output_module_html(module, outdir):
    src_file, stmts, excluded, missing, missing_display = coverage.analysis2(module)
    if not missing:
        return
    executed = list(set(stmts).difference(missing))
    total = list(set(stmts).union(excluded))
    total.sort()
    fo = file(os.path.join(outdir, module.__name__ + '.html'), 'w+')
    print >>fo, "source file: <b>%s</b><br>" %src_file
    print >>fo, "file stats: <b>%d lines, %d excluded, %d executed: %0.1f%% covered</b>" \
          %(len(total), len(excluded), len(executed), float(len(executed))/len(stmts)*100)
    print >>fo, "<pre>"
    for i, l in enumerate(l.rstrip() for l in open(src_file, 'rb').readlines()):
        color = 'gray'
        if i+1 in executed: color="green"
        if i+1 in excluded: color="blue"
        if i+1 in missing: color="red"
        print >>fo, '<font color="%s">%04s. %s</font>' %(color, i+1, cgi.escape(l))
    print >>fo, "</pre>"
    fo.close()
