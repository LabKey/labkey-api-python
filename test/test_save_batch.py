from __future__ import unicode_literals
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.utils import create_server_context
from labkey.experiment import save_batch, Batch, Run
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError
from mock_server_responses import MockSaveBatch


# We want to verify the request is properly formed
# and results/exceptions from a stock response are as expected
class TestInsertRows(unittest.TestCase):
    configs = {
        'protocol': 'https://'
        , 'server': 'my_testServer:8080'
        , 'context_path': 'testPath'
        , 'project_path': 'testProject/subfolder'
    }
    mock_service = MockSaveBatch(**configs)
    assay_id = 12345

    # Run data rows
    dataRows = [
        # {
        #     # ColumnName : Value
        #     "SampleId": "Monkey 1",
        #     "TimePoint": "2008/11/02 11:22:33",
        #     "DoubleData": 4.5,
        #     "HiddenData": "another data point"
        # }
        # , {
        #     "SampleId": "Monkey 2",
        #     "TimePoint": "2008/11/02 14:00:01",
        #     "DoubleData": 3.1,
        #     "HiddenData": "fozzy bear"
        # }, {
        #     "SampleId": "Monkey 3",
        #     "TimePoint": "2008/11/02 14:00:01",
        #     "DoubleData": 1.5,
        #     "HiddenData": "jimbo"
        # }
    ]

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

    _EXPECTED_URL = mock_service.get_server_url()
    _EXPECTED_DATA = '{"assayId": 12345, "batches": [{"batchProtocolId": 0, "comment": null, "created": null, "createdBy": null, "lsid": null, "modified": null, "modifiedBy": null, "name": null, "properties": {"PropertyName": "Property Value"}, "runs": [{"comment": null, "created": null, "createdBy": null, "dataInputs": [], "dataRows": [], "experiments": [], "filePathRoot": null, "lsid": null, "materialInputs": [], "materialOutputs": [], "modified": null, "modifiedBy": null, "name": "python upload", "properties": {"RunFieldName": "Run Field Value"}}]}]}'
    _EXPECTED_HEADERS = {'Accept': 'text/plain', 'Content-type': 'application/json'}

    def setUp(self):
        self.server_context = create_server_context(
            self.configs['server'], self.configs['project_path'], self.configs['context_path'])

    @mock.patch('labkey.utils.requests.Session.post')
    def test_success(self, mock_post):
        expected_response = self.mock_service.get_successful_response()
        mock_post.return_value = expected_response
        resp = save_batch(self.server_context, self.assay_id, self.batch)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_server_error(self, mock_post):
        with self.assertRaises(RequestError):
            mock_post.return_value = self.mock_service.get_general_error_response()
            save_batch(self.server_context, self.assay_id, self.batch)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_unauthorized(self, mock_post):
        with self.assertRaises(RequestAuthorizationError):
            mock_post.return_value = self.mock_service.get_unauthorized_response()
            save_batch(self.server_context, self.assay_id, self.batch)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_server_not_found(self, mock_post):
        with self.assertRaises(ServerNotFoundError):
            mock_post.return_value = self.mock_service.get_server_not_found_response()
            save_batch(self.server_context, self.assay_id, self.batch)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)

    @mock.patch('labkey.utils.requests.Session.post')
    def test_query_not_found(self, mock_post):
        with self.assertRaises(QueryNotFoundError):
            mock_post.return_value = self.mock_service.get_query_not_found_response()
            save_batch(self.server_context, self.assay_id, self.batch)

        mock_post.assert_called_with(self._EXPECTED_URL, data=self._EXPECTED_DATA,
                                     headers=self._EXPECTED_HEADERS)


if __name__ == '__main__':
    unittest.main()