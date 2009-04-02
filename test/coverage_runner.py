import coverage, os
from glob import glob
from inspect import getmodulename

from django.test.simple import run_tests as base_run_tests
from django.db.models import get_app, get_apps

def get_all_app_modules(app_module):
    """
    Returns all possible modules to report coverage on, even if they
    aren't loaded.
    """
    try:
        app_dirpath = os.path.split(app_module.__path__[0])[0]
    except AttributeError:
        app_dirpath = os.path.split(app_module.__file__)[0]

    mod_list = []
    for root, dirs, files in os.walk(app_dirpath):
        mod_list.extend(glob('%s/*.py' %root))

    return mod_list

def run_tests(test_labels, verbosity=1, interactive=True,
              extra_tests=[]):
    """
    Test runner which displays a code coverage report at the end of the
    run.
    """
    coverage.use_cache(0)
    coverage.start()
    results = base_run_tests(test_labels, verbosity, interactive, extra_tests)
    coverage.stop()

    coverage_modules = []
    if test_labels:
        for label in [l for l in test_labels if '.' not in l]:
            app = get_app(label)
            coverage_modules.extend(get_all_app_modules(app))
    else:
        for app in get_apps():
            coverage_modules.extend(get_all_app_modules(app))

    if coverage_modules:
        coverage.report(coverage_modules, show_missing=1)

    return results
