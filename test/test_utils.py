#
# Copyright (c) 2015-2016 LabKey Corporation
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
import requests

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.utils import create_server_context


def mock_server_context(mock_action):
    return create_server_context(mock_action.server_name, mock_action.project_path, mock_action.context_path)


def success_test(test, expected_response, api_method, compare_response, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.post') as mock_post:
        mock_post.return_value = expected_response
        resp = api_method(*args)

        # validate response is as expected
        if compare_response:
            test.assertEqual(resp, expected_response.text)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_post.assert_called_once_with(*expected_args, **expected_kwargs)


def success_test_get(test, expected_response, api_method, compare_response, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.get') as mock_get:
        mock_get.return_value = expected_response
        resp = api_method(*args)

        # validate response is as expected
        if compare_response:
            test.assertEqual(resp, expected_response.text)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_get.assert_called_once_with(*expected_args, **expected_kwargs)


def throws_error_test(test, expected_error, expected_response, api_method, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.post') as mock_post:
        with test.assertRaises(expected_error):
            mock_post.return_value = expected_response
            api_method(*args)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_post.assert_called_once_with(*expected_args, **expected_kwargs)


class MockLabKey:
    api = ""
    default_protocol = 'https://'
    default_server = 'my_testServer:8080'
    default_context_path = 'testPath'
    default_project_path = 'testProject/subfolder'
    default_action = 'query'
    default_success_body = ''
    default_unauthorized_body = ''
    default_server_not_found_body = ''
    default_query_not_found_body = ''
    default_general_server_error_body = ''

    def __init__(self, **kwargs):
        self.protocol = kwargs.pop('protocol', self.default_protocol)
        self.server_name = kwargs.pop('server_name', self.default_server)
        self.context_path = kwargs.pop('context_path', self.default_context_path)
        self.project_path = kwargs.pop('project_path', self.default_project_path)
        self.action = kwargs.pop('action', self.default_action)
        self.success_body = kwargs.pop('success_body', self.default_success_body)
        self.unauthorized_body = kwargs.pop('unauthorized_body', self.default_unauthorized_body)
        self.server_not_found_body = kwargs.pop('server_not_found_body', self.default_server_not_found_body)
        self.query_not_found_body = kwargs.pop('query_not_found_body', self.default_query_not_found_body)
        self.general_server_error_body = kwargs.pop('general_server_error_body', self.default_general_server_error_body)

    def _get_mock_response(self, code, url, body):
        mock_response = mock.Mock(requests.Response)
        mock_response.status_code = code
        mock_response.url = url
        mock_response.text = body
        mock_response.json.return_value = mock_response.text
        return mock_response

    def get_server_url(self):
        return self.protocol + '/'.join([self.server_name, self.context_path,
                                        self.action, self.project_path, self.api])

    def get_successful_response(self, code=200):
        return self._get_mock_response(code, self.get_server_url(), self.success_body)

    def get_unauthorized_response(self, code=401):
        return self._get_mock_response(code, self.get_server_url(), self.unauthorized_body)

    def get_server_not_found_response(self, code=404):
        response = self._get_mock_response(code, self.get_server_url(), self.server_not_found_body)
        # calling json() on empty response body causes a ValueError
        response.json.side_effect = ValueError()
        return response

    def get_query_not_found_response(self, code=404):
        return self._get_mock_response(code, self.get_server_url(), self.query_not_found_body)

    def get_general_error_response(self, code=500):
        return self._get_mock_response(code, self.get_server_url(), self.general_server_error_body)
