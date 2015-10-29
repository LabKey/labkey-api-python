from __future__ import unicode_literals
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.utils import create_server_context
from labkey.experiment import load_batch
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError
from mock_server_responses import MockLoadBatch


# We want to verify the request is properly formed
# and results/exceptions from a stock response are as expected
class TestInsertRows(unittest.TestCase):
    configs = {
        'protocol': 'https://'
        , 'server': 'my_testServer:8080'
        , 'context_path': 'testPath'
        , 'project_path': 'testProject/subfolder'
    }
    mock_service = MockLoadBatch(**configs)
    assay_id = 12345
    batch_id = 54321

    _EXPECTED_URL = mock_service.get_server_url()
    _EXPECTED_DATA = '{"assayId": 12345, "batchId": 54321}'
    _EXPECTED_HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    _EXPECTED_TIMEOUT = 30


    def setUp(self):
        self.server_context = create_server_context(
            self.configs['server'], self.configs['project_path'], self.configs['context_path'])

    @mock.patch('labkey.utils.requests.Session.post')
    def test_success(self, mock_post):
        expected_response = self.mock_service.get_successful_response()
        mock_post.return_value = expected_response
        resp = load_batch(self.server_context, self.assay_id, self.batch_id)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_server_error(self, mock_post):
        with self.assertRaises(RequestError):
            mock_post.return_value = self.mock_service.get_general_error_response()
            load_batch(self.server_context, self.assay_id, self.batch_id)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_unauthorized(self, mock_post):
        with self.assertRaises(RequestAuthorizationError):
            mock_post.return_value = self.mock_service.get_unauthorized_response()
            load_batch(self.server_context, self.assay_id, self.batch_id)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_server_not_found(self, mock_post):
        with self.assertRaises(ServerNotFoundError):
            mock_post.return_value = self.mock_service.get_server_not_found_response()
            load_batch(self.server_context, self.assay_id, self.batch_id)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_query_not_found(self, mock_post):
        with self.assertRaises(QueryNotFoundError):
            mock_post.return_value = self.mock_service.get_query_not_found_response()
            load_batch(self.server_context, self.assay_id, self.batch_id)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)


if __name__ == '__main__':
    unittest.main()