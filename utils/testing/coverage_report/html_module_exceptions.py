import os

def html_module_exceptions(filename, exceptions, template, long_desc):
    exception_list = []
    exceptions.sort()
    for module_name in exceptions:
        exception_list.append(template.EXCEPTION_LINE %vars())
    exception_list = os.linesep.join(exception_list)

    fo = file(filename, 'wb+')
    print >>fo, template.TOP
    print >>fo, template.CONTENT_HEADER
    print >>fo, template.CONTENT_BODY %vars()
    print >>fo, template.BOTTOM
    fo.close()
