import coverage, coverage_html, imp, os, re, sys
from glob import glob

from django.conf import settings
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import get_app, get_apps
from django.test.simple import run_tests as base_run_tests

try:
    set
except:
    from sets import Set as set


RE_BLACKLIST = list()
for expr in getattr(settings, 'COVERAGE_TEST_PATH_BLACKLIST', []):
    RE_BLACKLIST.append(re.compile(expr))

def modules_from_pyfiles(root, pyfiles):
    if not pyfiles:
        return
    sys_path = [os.path.abspath(p) for p in sys.path]
    sys_path.sort()
    sys_path.reverse()
    test_module = os.path.basename(pyfiles[0])[:-3]
    for p in [p for p in sys_path if root.startswith(p)]:
        package = root.replace(p, '')
        package = '.'.join([e for e in package.split(os.path.sep) if e])
        try:
            module = __import__('.'.join([package,test_module]))
            break
        except (ImportError, AlreadyRegistered):
            package = None
    if package:
        for m_name in [os.path.basename(f)[:-3] for f in pyfiles]:
            m_fullname = '.'.join([package, m_name])
            f, fn, desc = imp.find_module(m_name, [root])
            try:
                yield imp.load_module(m_fullname, f, fn, desc)
            except AlreadyRegistered:
                pass # This is a Django admin definition module

def remove_blacklisted(pathlist):
    for p in pathlist:
        for r in RE_BLACKLIST:
            if r.search(p):
                pathlist.remove(p)
                break
    return pathlist

def remove_dirs(root, dirlist):
    dirlist = [os.path.join(root, d) for d in dirlist]
    dirlist = remove_blacklisted(dirlist)
    return [os.path.basename(d) for d in dirlist]

def get_all_app_modules(app_module):
    """
    Returns all possible modules to report coverage on, even if they
    aren't loaded.
    """
    try:
        app_dirpath = os.path.split(app_module.__path__[0])[0]
    except AttributeError:
        app_dirpath = os.path.split(app_module.__file__)[0]

    modules = list()
    paths = list()
    for root, dirs, files in os.walk(app_dirpath):
        dirs = remove_dirs(root, dirs)
        stop = False
        for r in RE_BLACKLIST:
            if r.search(root):
                stop = True
                break
        if stop: continue

        pyfiles = remove_blacklisted(glob('%s/*.py' %root))
        paths.extend(pyfiles)
        modules.extend(modules_from_pyfiles(root, pyfiles))
    return paths, modules

def run_tests(test_labels, verbosity=1, interactive=True,
              extra_tests=[]):
    """
    Test runner which displays a code coverage report at the end of the
    run.
    """
    coverage.use_cache(0)
    for e in getattr(settings, 'COVERAGE_TEST_EXCLUDES', []):
        coverage.exclude(e)
    coverage.start()
    results = base_run_tests(test_labels, verbosity, interactive, extra_tests)
    coverage.stop()

    coverage_modules = set()
    coverage_paths = set()
    if test_labels:
        for label in test_labels:
            label = label.split('.')[0]
            app = get_app(label)
            p, m = get_all_app_modules(app)
            coverage_paths.update(p)
            coverage_modules.update(m)
    else:
        for app in get_apps():
            p, m = get_all_app_modules(app)
            coverage_paths.update(p)
            coverage_modules.update(m)

    if getattr(settings, 'COVERAGE_TEST_LIST_STYLE', '').lower() == 'path' and coverage_paths:
        coverage.report(list(coverage_paths), show_missing=1)
    elif coverage_modules:
        coverage.report(list(coverage_modules), show_missing=1)

##    for module in coverage_modules:
##        f, s, m, mf = coverage.analysis(module)
##        fo = file(os.path.join('test_html', module.__name__ + '.html'), 'w+')
##        coverage_html.colorize_file(f, outstream=fo, not_covered=mf)
##        fo.close()

    return results
