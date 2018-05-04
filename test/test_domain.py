#
# Copyright (c) 2018 LabKey Corporation
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
import json
import os
import tempfile
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey import utils
from labkey.domain import create, Domain, drop, get, infer_fields, save
from labkey.exceptions import RequestAuthorizationError

from test_utils import MockLabKey, mock_server_context, success_test, success_test_get, throws_error_test, throws_error_test_get


domain_controller = 'property'


class TestCreate(unittest.TestCase):

    def setUp(self):

        domain_definition = {
            'kind': 'IntList',
            'domainDesign': {
                'name': 'TheTestList',
                'fields': [{
                    'name': 'theKey',
                    'rangeURI': 'int'
                }]
            },
            'options': {
                'keyName': 'theKey'
            }
        }

        class MockCreate(MockLabKey):
            api = 'createDomain.api'
            default_action = domain_controller
            default_success_body = domain_definition

        self.service = MockCreate()

        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': json.dumps(domain_definition),
            'headers': {'Content-Type': 'application/json'},
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), domain_definition
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(),
                     create, False,  *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          create, *self.args, **self.expected_kwargs)


class TestDrop(unittest.TestCase):
    schema_name = 'lists'
    query_name = 'TheTestList'

    def setUp(self):

        class MockDrop(MockLabKey):
            api = 'deleteDomain.api'
            default_action = domain_controller
            default_success_body = {}

        self.service = MockDrop()

        payload = {
            'schemaName': self.schema_name,
            'queryName': self.query_name
        }

        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': json.dumps(payload),
            'headers': {'Content-Type': 'application/json'},
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), self.schema_name, self.query_name
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(),
                     drop, False,  *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          drop, *self.args, **self.expected_kwargs)


class TestGet(unittest.TestCase):
    schema_name = 'lists'
    query_name = 'TheTestList'

    def setUp(self):

        class MockGet(MockLabKey):
            api = 'getDomain.api'
            default_action = domain_controller
            default_success_body = {}

        self.service = MockGet()

        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'headers': None,
            'params': {'schemaName': self.schema_name, 'queryName': self.query_name},
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), self.schema_name, self.query_name
        ]

    def test_success(self):
        test = self
        success_test_get(test, self.service.get_successful_response(),
                         get, False,  *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test_get(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                              get, *self.args, **self.expected_kwargs)


class TestInferFields(unittest.TestCase):

    def setUp(self):

        class MockInferFields(MockLabKey):
            api = 'inferDomain.api'
            default_action = domain_controller
            default_success_body = {}

        self.service = MockInferFields()

        self.fd, self.path = tempfile.mkstemp()
        with os.fdopen(self.fd, 'w') as tmp:
            tmp.write('Name\tAge\nNick\t32\nBrian\t27\n')
            self.file = tmp

        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': None,
            'files': {'inferfile': self.file},
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), self.file
        ]

    def tearDown(self):
        os.remove(self.path)

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(),
                     infer_fields, False,  *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          infer_fields, *self.args, **self.expected_kwargs)


class TestSave(unittest.TestCase):
    domain = Domain(**{
        'container': 'TestContainer',
        'description': 'A Test Domain',
        'domain_id': 9823
    })
    schema_name = 'lists'
    query_name = 'TheTestList'

    def setUp(self):

        class MockSave(MockLabKey):
            api = 'saveDomain.api'
            default_action = domain_controller
            default_success_body = {}

        self.service = MockSave()

        payload = {
            'domainDesign': self.domain.to_json(),
            'queryName': self.query_name,
            'schemaName': self.schema_name
        }

        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': json.dumps(payload),
            'headers': {'Content-Type': 'application/json'},
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), self.schema_name, self.query_name, self.domain
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(),
                     save, False,  *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          save, *self.args, **self.expected_kwargs)


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite([
        load_tests(TestCreate),
        load_tests(TestDrop),
        load_tests(TestGet),
        load_tests(TestInferFields),
        load_tests(TestSave)
    ])


if __name__ == '__main__':
    utils.DISABLE_CSRF_CHECK = True
    unittest.main()
