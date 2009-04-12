import sys

from django.test import simple

from test_registration import Register

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    total_tests = simple.run_tests(test_labels, verbosity, interactive, extra_tests)
    
    print >>sys.stdout
    print >>sys.stdout, 'Tested the following:'
    for t in Register.tested:
        print >>sys.stdout, ' * %s' %t
    return total_tests
