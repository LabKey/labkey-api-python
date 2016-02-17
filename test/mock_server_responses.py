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
"""
Example server responses to be used for mocking
"""
from __future__ import unicode_literals
import requests


try:
    import mock
except ImportError:
    import unittest.mock as mock


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


class MockSelectRows(MockLabKey):
    api = 'getQuery.api'
    default_success_body = '{"columnModel": [{"align": "right", "dataIndex": "Participant ID", "editable": true , "header": "Participant ID", "hidden": false , "required": false , "scale": 10 , "sortable": true , "width": 60 }] , "formatVersion": 8.3 , "metaData": {"description": null , "fields": [{"autoIncrement": false , "calculated": false , "caption": "Participant ID", "conceptURI": null , "defaultScale": "LINEAR", "defaultValue": null , "dimension": false , "excludeFromShifting": false , "ext": {} , "facetingBehaviorType": "AUTOMATIC", "fieldKey": "Participant ID", "fieldKeyArray": ["Participant ID"] , "fieldKeyPath": "Participant ID", "friendlyType": "Integer", "hidden": false , "inputType": "text", "isAutoIncrement": false , "isHidden": false , "isKeyField": false , "isMvEnabled": false , "isNullable": true , "isReadOnly": false , "isSelectable": true , "isUserEditable": true , "isVersionField": false , "jsonType": "int", "keyField": false , "measure": false , "mvEnabled": false , "name": "Participant ID", "nullable": true , "protected": false , "rangeURI": "http://www.w3.org/2001/XMLSchema#int", "readOnly": false , "recommendedVariable": false , "required": false , "selectable": true , "shortCaption": "Participant ID", "shownInDetailsView": true , "shownInInsertView": true , "shownInUpdateView": true , "sqlType": "int", "type": "int", "userEditable": true , "versionField": false }] , "id": "Key", "importMessage": null , "importTemplates": [{"label": "Download Template", "url": ""}] , "root": "rows", "title": "Demographics", "totalProperty": "rowCount"} , "queryName": "Demographics", "rowCount": 224 , "rows": [{	"Participant ID": 133428 } , {	"Participant ID": 138488 } , {	"Participant ID": 140163 } , {	"Participant ID": 144740 } , {	"Participant ID": 150489 } ] , "schemaName": "lists"}'


class MockInsertRows(MockLabKey):
    api = 'insertRows.api'


class MockDeleteRows(MockLabKey):
    api = 'deleteRows.api'


class MockExecuteSQL(MockLabKey):
    api = 'executeSql.api'


class MockUpdateRows(MockLabKey):
    api = 'updateRows.api'


class MockLoadBatch(MockLabKey):
    api = 'getAssayBatch.api'
    default_action = 'assay'
    default_success_body = {"assayId": 2809, "batch": {"lsid": "urn:lsid:labkey.com:Experiment.Folder-1721:465ad7db-58d8-1033-a587-7eb0c02c2efe", "createdBy": "", "created": "2015/10/19 18:21:57", "name": "python batch", "modified": "2015/10/19 18:21:57", "modifiedBy": "", "comment": None, "id": 120, "runs": [{"dataOutputs": [], "dataRows": [{"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}], "dataInputs": [], "created": "2015/10/19 18:21:57", "materialInputs": [{"lsid": "urn:lsid:labkey.com:AssayRunMaterial.Folder-1721:Unknown", "role": "Sample", "created": "2015/10/19 18:21:57", "name": "Unknown", "modified": "2015/10/19 18:21:57", "id": 7641}], "lsid": "urn:lsid:labkey.com:GeneralAssayRun.Folder-1721:465ad7dd-58d8-1033-a587-7eb0c02c2efe", "materialOutputs": [], "createdBy": "", "name": "python upload", "modified": "2015/10/19 18:21:57", "modifiedBy": "", "comment": None, "id": 1526, "properties": {}}], "properties": {"ParticipantVisitResolver": None, "TargetStudy": None}}}


class MockSaveBatch(MockLabKey):
    api = 'saveAssayBatch.api'
    default_action = 'assay'
    default_success_body = {"batches": [{"lsid": "urn:lsid:labkey.com:Experiment.Folder-1721:50666e45-609f-1033-ba4a-ca4935e31f28", "createdBy": "", "created": "2015/10/29 12:17:50", "name": "python batch 7", "modified": "2015/10/29 12:17:51", "modifiedBy": "", "comment": None, "id": 139, "runs": [{"dataOutputs": [], "dataRows": [{"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}, {"Treatment Group": None, "Start Date": None, "Height _inches_": None, "Comments": None, "Status of Infection": None, "Country": None, "Gender": None, "Group Assignment": None, "Participant ID": None, "Date": None}], "dataInputs": [], "created": "2015/10/29 12:17:50", "materialInputs": [{"lsid": "urn:lsid:labkey.com:AssayRunMaterial.Folder-1721:Unknown", "role": "Sample", "created": "2015/10/19 18:21:57", "name": "Unknown", "modified": "2015/10/19 18:21:57", "id": 7641}], "lsid": "urn:lsid:labkey.com:GeneralAssayRun.Folder-1721:50666e47-609f-1033-ba4a-ca4935e31f28", "materialOutputs": [], "createdBy": "", "name": "python upload", "modified": "2015/10/29 12:17:51", "modifiedBy": "", "comment": None, "id": 1673, "properties": {}}], "properties": {"ParticipantVisitResolver": None, "TargetStudy": None}}], "assayId": 2809}


