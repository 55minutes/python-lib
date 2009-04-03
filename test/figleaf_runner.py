import figleaf, sys

from django.test import simple

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    figleaf.start()
    total_tests = simple.run_tests(test_labels, verbosity, interactive, extra_tests)
    figleaf.stop()
    figleaf.write_coverage('.figleaf')
    return total_tests
