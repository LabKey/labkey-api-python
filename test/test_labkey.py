from __future__ import unicode_literals
import unittest

from test_experiment_api import suite as exp_suite
from test_query_api import suite as query_suite

if __name__ == '__main__':
    all_tests = unittest.TestSuite([
        exp_suite(),
        query_suite()
    ])
    unittest.TextTestRunner().run(all_tests)