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
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.query import delete_rows, update_rows, insert_rows, select_rows, execute_sql
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError

from test_utils import MockLabKey, mock_server_context, success_test, throws_error_test


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


schema = 'testSchema'
query = 'testQuery'


class TestDeleteRows(unittest.TestCase):

    def setUp(self):
        self.service = MockDeleteRows()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"queryName": "' + query + '", "rows": "{id:1234}", "schemaName": "' + schema + '"}'
            , 'headers': {u'Content-Type': u'application/json'}
            , 'timeout': 300
        }

        rows = '{id:1234}'
        self.args = [
            mock_server_context(self.service), schema, query, rows
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), delete_rows, True, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , delete_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , delete_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , delete_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , delete_rows, *self.args, **self.expected_kwargs)


class TestUpdateRows(unittest.TestCase):

    def setUp(self):
        self.service = MockUpdateRows()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"queryName": "' + query + '", "rows": "{id:1234}", "schemaName": "' + schema + '"}'
            , 'headers': {u'Content-Type': u'application/json'}
            , 'timeout': 300
        }

        rows = '{id:1234}'
        self.args = [
            mock_server_context(self.service), schema, query, rows
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), update_rows, True, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , update_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , update_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , update_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , update_rows, *self.args, **self.expected_kwargs)


class TestInsertRows(unittest.TestCase):

    def setUp(self):
        self.service = MockInsertRows()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"queryName": "' + query + '", "rows": "{id:1234}", "schemaName": "' + schema + '"}'
            , 'headers': {u'Content-Type': u'application/json'}
            , 'timeout': 300
        }

        rows = '{id:1234}'
        self.args = [
            mock_server_context(self.service), schema, query, rows
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), insert_rows, True, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , insert_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , insert_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , insert_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , insert_rows, *self.args, **self.expected_kwargs)


class TestExecuteSQL(unittest.TestCase):

    def setUp(self):
        self.service = MockExecuteSQL()
        sql = 'select * from ' + schema + '.' + query
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': {'sql': sql, "schemaName": schema}
            , 'headers': None
            , 'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), schema, sql
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), execute_sql, True, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , execute_sql, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , execute_sql, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , execute_sql, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , execute_sql, *self.args, **self.expected_kwargs)


class TestSelectRows(unittest.TestCase):

    def setUp(self):
        self.service = MockSelectRows()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': {"schemaName": schema, "query.queryName": query}
            , 'headers': None
            , 'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), schema, query
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), select_rows, True, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , select_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , select_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , select_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , select_rows, *self.args, **self.expected_kwargs)


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite([
        load_tests(TestDeleteRows),
        load_tests(TestUpdateRows),
        load_tests(TestInsertRows),
        load_tests(TestExecuteSQL),
        load_tests(TestSelectRows)
    ])

if __name__ == '__main__':
    unittest.main()
