#
# Copyright (c) 2016-2017 LabKey Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import unicode_literals
import unittest

from labkey import utils
from test_domain import suite as domain_suite
from test_experiment_api import suite as exp_suite
from test_query_api import suite as query_suite
from test_security import suite as security_suite
from test_unsupported import suite as unsupported_suite

if __name__ == '__main__':

    # The mocks in the tests expect a request only to be made to the appropriate action.
    # This flag disables the CSRF check built into ServerContext.make_request() so the tests
    # get consistent results.
    utils.DISABLE_CSRF_CHECK = True

    all_tests = unittest.TestSuite([
        domain_suite(),
        exp_suite(),
        query_suite(),
        security_suite(),
        unsupported_suite()
    ])
    unittest.TextTestRunner().run(all_tests)
