import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))

def make_and_get_suite(test_modules):
    suite = unittest.TestSuite()

    for test_module in test_modules:
        try:
            module = __import__(test_module, globals(), locals(), ['suite'])
            suite_fn = getattr(module, 'suite')
            suite.addTest(suite_fn())
        except (ImportError, AttributeError):
            all_tests = unittest.defaultTestLoader.loadTestsFromName(test_module)
            suite.addTest(all_tests)

    return suite

def test_modules():
    """Returns a list of names of the test modules"""
    return ['test_linkedlist']

if __name__ == '__main__':
    suite = make_and_get_suite(test_modules())
    unittest.TextTestRunner().run(suite)