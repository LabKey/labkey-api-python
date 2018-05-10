#
# Copyright (c) 2015-2017 LabKey Corporation
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

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey import utils
from labkey.experiment import load_batch, save_batch, Batch, Run
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError

from test_utils import MockLabKey, mock_server_context, success_test, throws_error_test


class MockLoadBatch(MockLabKey):
    api = 'getAssayBatch.api'
    default_action = 'assay'
    default_success_body = {"assayId": 2809, "batch": {"lsid": "urn:lsid:labkey.com:Experiment.Folder-1721:465ad7db-58d8-1033-a587-7eb0c02c2efe", "createdBy": "", "created": "2015/10/19 18:21:57", "name": "python batch", "modified": "2015/10/19 18:21:57", "modifiedBy": "", "comment": None, "id": 120, "runs": [{"dataOutputs": [], "dataRows": [{"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}], "dataInputs": [], "created": "2015/10/19 18:21:57", "materialInputs": [{"lsid": "urn:lsid:labkey.com:AssayRunMaterial.Folder-1721:Unknown", "role": "Sample", "created": "2015/10/19 18:21:57", "name": "Unknown", "modified": "2015/10/19 18:21:57", "id": 7641}], "lsid": "urn:lsid:labkey.com:GeneralAssayRun.Folder-1721:465ad7dd-58d8-1033-a587-7eb0c02c2efe", "materialOutputs": [], "createdBy": "", "name": "python upload", "modified": "2015/10/19 18:21:57", "modifiedBy": "", "comment": None, "id": 1526, "properties": {}}], "properties": {"ParticipantVisitResolver": None, "TargetStudy": None}}}


class MockSaveBatch(MockLabKey):
    api = 'saveAssayBatch.api'
    default_action = 'assay'
    default_success_body = {"batches": [{"lsid": "urn:lsid:labkey.com:Experiment.Folder-1721:50666e45-609f-1033-ba4a-ca4935e31f28", "createdBy": "", "created": "2015/10/29 12:17:50", "name": "python batch 7", "modified": "2015/10/29 12:17:51", "modifiedBy": "", "comment": None, "id": 139, "runs": [{"dataOutputs": [], "dataRows": [{"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}], "dataInputs": [], "created": "2015/10/29 12:17:50", "materialInputs": [{"lsid": "urn:lsid:labkey.com:AssayRunMaterial.Folder-1721:Unknown", "role": "Sample", "created": "2015/10/19 18:21:57", "name": "Unknown", "modified": "2015/10/19 18:21:57", "id": 7641}], "lsid": "urn:lsid:labkey.com:GeneralAssayRun.Folder-1721:50666e47-609f-1033-ba4a-ca4935e31f28", "materialOutputs": [], "createdBy": "", "name": "python upload", "modified": "2015/10/29 12:17:51", "modifiedBy": "", "comment": None, "id": 1673, "properties": {}}], "properties": {"ParticipantVisitResolver": None, "TargetStudy": None}}], "assayId": 2809}


assay_id = 12345
batch_id = 54321


class TestLoadBatch(unittest.TestCase):

    def setUp(self):
        self.service = MockLoadBatch()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': '{"assayId": 12345, "batchId": 54321}',
            'headers': {'Content-type': 'application/json', 'Accept': 'text/plain'},
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), assay_id, batch_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), load_batch, False, *self.args, **self.expected_kwargs)

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

        data_rows = []

        # Generate the Run object(s)
        run = Run()
        run.name = 'python upload'
        run.data_rows = data_rows
        run.properties['RunFieldName'] = 'Run Field Value'

        # Generate the Batch object(s)
        batch = Batch()
        batch.runs = [run]
        batch.properties['PropertyName'] = 'Property Value'

        self.service = MockSaveBatch()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': '{"assayId": 12345, "batches": [{"batchProtocolId": 0, "comment": null, "created": null, "createdBy": null, "modified": null, "modifiedBy": null, "name": null, "properties": {"PropertyName": "Property Value"}, "runs": [{"comment": null, "created": null, "createdBy": null, "dataInputs": [], "dataRows": [], "experiments": [], "filePathRoot": null, "materialInputs": [], "materialOutputs": [], "modified": null, "modifiedBy": null, "name": "python upload", "properties": {"RunFieldName": "Run Field Value"}}]}]}',
            'headers': {'Content-type': 'application/json', 'Accept': 'text/plain'},
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), assay_id, batch
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), save_batch, False, *self.args, **self.expected_kwargs)

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


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite([
        load_tests(TestLoadBatch),
        load_tests(TestSaveBatch)
    ])


if __name__ == '__main__':
    utils.DISABLE_CSRF_CHECK = True
    unittest.main()
