from __future__ import unicode_literals
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.utils import create_server_context
from labkey.query import select_rows
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError
from mock_server_responses import MockSelectRows


# We want to verify the request is properly formed
# and results/exceptions from a stock response are as expected
class TestSelectRows(unittest.TestCase):
    schema = 'testSchema'
    query = 'testQuery'
    configs = {
        'protocol': 'https://'
        , 'server': 'my_testServer:8080'
        , 'context_path': 'testPath'
        , 'project_path': 'testProject/subfolder'
    }
    mock_service = MockSelectRows(schema, query, **configs)
    _EXPECTED_URL = mock_service.get_server_url()
    _EXPECTED_DATA = {"query.queryName": 'testQuery', 'schemaName': 'testSchema'}
    _EXPECTED_HEADERS = None
    _EXPECTED_TIMEOUT = 30

    def setUp(self):
        self.server_context = create_server_context(
            self.configs['server'], self.configs['project_path'], self.configs['context_path'])

    @mock.patch('labkey.utils.requests.Session.post')
    def test_success(self, mock_post):
        expected_response = self.mock_service.get_successful_response()
        mock_post.return_value = expected_response
        resp = select_rows(self.server_context, self.schema, self.query)

        self.assertEquals(resp, expected_response.text)
        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS, timeout=self._EXPECTED_TIMEOUT)
    # TODO: Add additional parameter tests

    @mock.patch('labkey.utils.requests.Session.post')
    def test_server_error(self, mock_post):
        with self.assertRaises(RequestError):
            mock_post.return_value = self.mock_service.get_general_error_response()
            select_rows(self.server_context, self.schema, self.query)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS, timeout=self._EXPECTED_TIMEOUT)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_unauthorized(self, mock_post):
        with self.assertRaises(RequestAuthorizationError):
            mock_post.return_value = self.mock_service.get_unauthorized_response()
            select_rows(self.server_context, self.schema, self.query)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS, timeout=self._EXPECTED_TIMEOUT)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_server_not_found(self, mock_post):
        with self.assertRaises(ServerNotFoundError):
            mock_post.return_value = self.mock_service.get_server_not_found_response()
            select_rows(self.server_context, self.schema, self.query)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS, timeout=self._EXPECTED_TIMEOUT)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_query_not_found(self, mock_post):
        with self.assertRaises(QueryNotFoundError):
            mock_post.return_value = self.mock_service.get_query_not_found_response()
            select_rows(self.server_context, self.schema, self.query)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS, timeout=self._EXPECTED_TIMEOUT)


if __name__ == '__main__':
    unittest.main()
