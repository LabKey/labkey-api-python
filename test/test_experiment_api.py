from __future__ import unicode_literals
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.utils import create_server_context
from labkey.experiment import load_batch, save_batch, Batch, Run
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError
from mock_server_responses import MockLoadBatch, MockSaveBatch


def success_test(test, expected_response, api_method, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.post') as mock_post:
        mock_post.return_value = expected_response
        resp = api_method(*args)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_post.assert_called_once_with(*expected_args, **expected_kwargs)


def throws_error_test(test, expected_error, expected_response, api_method, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.post') as mock_post:
        with test.assertRaises(expected_error):
            mock_post.return_value = expected_response
            api_method(*args)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_post.assert_called_once_with(*expected_args, **expected_kwargs)


configs = {
    'protocol': 'https://'
    , 'server': 'my_testServer:8080'
    , 'context_path': 'testPath'
    , 'project_path': 'testProject/subfolder'
}

assay_id = 12345
batch_id = 54321
server_context = create_server_context(configs['server'], configs['project_path'], configs['context_path'])


class TestLoadBatch(unittest.TestCase):

    def setUp(self):
        self.configs = configs.copy()
        self.service = MockLoadBatch(**self.configs)
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"assayId": 12345, "batchId": 54321}'
            , 'headers': {'Content-type': 'application/json', 'Accept': 'text/plain'}
        }

        self.args = [
            server_context, assay_id, batch_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), load_batch, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , load_batch, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , load_batch, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , load_batch, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , load_batch, *self.args, **self.expected_kwargs)


class TestSaveBatch(unittest.TestCase):

    def setUp(self):

        dataRows = []

        # Generate the Run object(s)
        runTest = Run()
        runTest.name = 'python upload'
        runTest.data_rows = dataRows
        runTest.properties['RunFieldName'] = 'Run Field Value'

        # Generate the Batch object(s)
        batch = Batch()
        batch.runs = [runTest]
        # batch.name = 'python batch'
        batch.properties['PropertyName'] = 'Property Value'

        self.configs = configs.copy()
        self.service = MockSaveBatch(**self.configs)
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"assayId": 12345, "batches": [{"batchProtocolId": 0, "comment": null, "created": null, "createdBy": null, "lsid": null, "modified": null, "modifiedBy": null, "name": null, "properties": {"PropertyName": "Property Value"}, "runs": [{"comment": null, "created": null, "createdBy": null, "dataInputs": [], "dataRows": [], "experiments": [], "filePathRoot": null, "lsid": null, "materialInputs": [], "materialOutputs": [], "modified": null, "modifiedBy": null, "name": "python upload", "properties": {"RunFieldName": "Run Field Value"}}]}]}'
            , 'headers': {'Content-type': 'application/json', 'Accept': 'text/plain'}
        }

        self.args = [
            server_context, assay_id, batch
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), save_batch, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , save_batch, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , save_batch, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , save_batch, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , save_batch, *self.args, **self.expected_kwargs)