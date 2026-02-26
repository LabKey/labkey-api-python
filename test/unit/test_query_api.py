#
# Copyright (c) 2015-2018 LabKey Corporation
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
import json
import unittest

from labkey.query import (
    delete_rows,
    update_rows,
    insert_rows,
    save_rows,
    select_rows,
    execute_sql,
    QueryFilter,
)
from labkey.exceptions import (
    RequestError,
    QueryNotFoundError,
    ServerNotFoundError,
    RequestAuthorizationError,
)
from labkey.utils import waf_encode

from .utilities import MockLabKey, mock_server_context, success_test, throws_error_test


class MockSelectRows(MockLabKey):
    api = "getQuery.api"
    default_success_body = '{"columnModel": [{"align": "right", "dataIndex": "Participant ID", "editable": true , "header": "Participant ID", "hidden": false , "required": false , "scale": 10 , "sortable": true , "width": 60 }] , "formatVersion": 8.3 , "metaData": {"description": null , "fields": [{"autoIncrement": false , "calculated": false , "caption": "Participant ID", "conceptURI": null , "defaultScale": "LINEAR", "defaultValue": null , "dimension": false , "excludeFromShifting": false , "ext": {} , "facetingBehaviorType": "AUTOMATIC", "fieldKey": "Participant ID", "fieldKeyArray": ["Participant ID"] , "fieldKeyPath": "Participant ID", "friendlyType": "Integer", "hidden": false , "inputType": "text", "isAutoIncrement": false , "isHidden": false , "isKeyField": false , "isMvEnabled": false , "isNullable": true , "isReadOnly": false , "isSelectable": true , "isUserEditable": true , "isVersionField": false , "jsonType": "int", "keyField": false , "measure": false , "mvEnabled": false , "name": "Participant ID", "nullable": true , "protected": false , "rangeURI": "http://www.w3.org/2001/XMLSchema#int", "readOnly": false , "recommendedVariable": false , "required": false , "selectable": true , "shortCaption": "Participant ID", "shownInDetailsView": true , "shownInInsertView": true , "shownInUpdateView": true , "sqlType": "int", "type": "int", "userEditable": true , "versionField": false }] , "id": "Key", "importMessage": null , "importTemplates": [{"label": "Download Template", "url": ""}] , "root": "rows", "title": "Demographics", "totalProperty": "rowCount"} , "queryName": "Demographics", "rowCount": 224 , "rows": [{	"Participant ID": 133428 } , {	"Participant ID": 138488 } , {	"Participant ID": 140163 } , {	"Participant ID": 144740 } , {	"Participant ID": 150489 } ] , "schemaName": "lists"}'


class MockInsertRows(MockLabKey):
    api = "insertRows.api"


class MockDeleteRows(MockLabKey):
    api = "deleteRows.api"


class MockExecuteSQL(MockLabKey):
    api = "executeSql.api"


class MockUpdateRows(MockLabKey):
    api = "updateRows.api"


class MockSaveRows(MockLabKey):
    api = "saveRows.api"


schema = "testSchema"
query = "testQuery"


class TestDeleteRows(unittest.TestCase):
    def setUp(self):
        self.service = MockDeleteRows()

        rows = "{id:1234}"

        self.expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": '{"queryName": "'
            + query
            + '", "rows": "'
            + rows
            + '", "schemaName": "'
            + schema
            + '"}',
            "headers": {"Content-Type": "application/json"},
            "timeout": 300,
            "allow_redirects": False,
        }

        self.args = [mock_server_context(self.service), schema, query, rows]

    def test_success(self):
        test = self
        success_test(
            test,
            self.service.get_successful_response(),
            delete_rows,
            True,
            *self.args,
            **self.expected_kwargs,
        )

    def test_unauthorized(self):
        test = self
        throws_error_test(
            test,
            RequestAuthorizationError,
            self.service.get_unauthorized_response(),
            delete_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_not_found(self):
        test = self
        throws_error_test(
            test,
            QueryNotFoundError,
            self.service.get_query_not_found_response(),
            delete_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_server_not_found(self):
        test = self
        throws_error_test(
            test,
            ServerNotFoundError,
            self.service.get_server_not_found_response(),
            delete_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_general_error(self):
        test = self
        throws_error_test(
            test,
            RequestError,
            self.service.get_general_error_response(),
            delete_rows,
            *self.args,
            **self.expected_kwargs,
        )


class TestUpdateRows(unittest.TestCase):
    def setUp(self):
        self.service = MockUpdateRows()

        rows = "{id:1234}"

        self.expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": '{"queryName": "'
            + query
            + '", "rows": "'
            + rows
            + '", "schemaName": "'
            + schema
            + '"}',
            "headers": {"Content-Type": "application/json"},
            "timeout": 300,
            "allow_redirects": False,
        }

        self.args = [mock_server_context(self.service), schema, query, rows]

    def test_success(self):
        test = self
        success_test(
            test,
            self.service.get_successful_response(),
            update_rows,
            True,
            *self.args,
            **self.expected_kwargs,
        )

    def test_unauthorized(self):
        test = self
        throws_error_test(
            test,
            RequestAuthorizationError,
            self.service.get_unauthorized_response(),
            update_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_not_found(self):
        test = self
        throws_error_test(
            test,
            QueryNotFoundError,
            self.service.get_query_not_found_response(),
            update_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_server_not_found(self):
        test = self
        throws_error_test(
            test,
            ServerNotFoundError,
            self.service.get_server_not_found_response(),
            update_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_general_error(self):
        test = self
        throws_error_test(
            test,
            RequestError,
            self.service.get_general_error_response(),
            update_rows,
            *self.args,
            **self.expected_kwargs,
        )


class TestInsertRows(unittest.TestCase):
    def setUp(self):
        self.service = MockInsertRows()

        rows = "{id:1234}"

        self.expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": '{"queryName": "'
            + query
            + '", "rows": "'
            + rows
            + '", "schemaName": "'
            + schema
            + '"}',
            "headers": {"Content-Type": "application/json"},
            "timeout": 300,
            "allow_redirects": False,
        }

        self.args = [mock_server_context(self.service), schema, query, rows]

    def test_success(self):
        test = self
        success_test(
            test,
            self.service.get_successful_response(),
            insert_rows,
            True,
            *self.args,
            **self.expected_kwargs,
        )

    def test_unauthorized(self):
        test = self
        throws_error_test(
            test,
            RequestAuthorizationError,
            self.service.get_unauthorized_response(),
            insert_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_not_found(self):
        test = self
        throws_error_test(
            test,
            QueryNotFoundError,
            self.service.get_query_not_found_response(),
            insert_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_server_not_found(self):
        test = self
        throws_error_test(
            test,
            ServerNotFoundError,
            self.service.get_server_not_found_response(),
            insert_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_general_error(self):
        test = self
        throws_error_test(
            test,
            RequestError,
            self.service.get_general_error_response(),
            insert_rows,
            *self.args,
            **self.expected_kwargs,
        )


class TestExecuteSQL(unittest.TestCase):
    def setUp(self):
        self.service = MockExecuteSQL()
        sql = "select * from " + schema + "." + query
        self.expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": {"sql": waf_encode(sql), "schemaName": schema},
            "headers": None,
            "timeout": 300,
            "allow_redirects": False,
        }

        self.args = [mock_server_context(self.service), schema, sql]

    def test_success(self):
        test = self
        success_test(
            test,
            self.service.get_successful_response(),
            execute_sql,
            True,
            *self.args,
            **self.expected_kwargs,
        )

    def test_unauthorized(self):
        test = self
        throws_error_test(
            test,
            RequestAuthorizationError,
            self.service.get_unauthorized_response(),
            execute_sql,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_not_found(self):
        test = self
        throws_error_test(
            test,
            QueryNotFoundError,
            self.service.get_query_not_found_response(),
            execute_sql,
            *self.args,
            **self.expected_kwargs,
        )

    def test_server_not_found(self):
        test = self
        throws_error_test(
            test,
            ServerNotFoundError,
            self.service.get_server_not_found_response(),
            execute_sql,
            *self.args,
            **self.expected_kwargs,
        )

    def test_general_error(self):
        test = self
        throws_error_test(
            test,
            RequestError,
            self.service.get_general_error_response(),
            execute_sql,
            *self.args,
            **self.expected_kwargs,
        )


class TestSelectRows(unittest.TestCase):
    def setUp(self):
        self.service = MockSelectRows()
        self.expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": {"schemaName": schema, "query.queryName": query, "query.maxRows": -1},
            "headers": None,
            "timeout": 300,
            "allow_redirects": False,
        }

        self.args = [mock_server_context(self.service), schema, query]

    def test_success(self):
        test = self
        success_test(
            test,
            self.service.get_successful_response(),
            select_rows,
            True,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_filter(self):
        test = self
        view_name = None
        filter_array = [
            QueryFilter("Field1", "value", "eq"),
            QueryFilter("Field2", "value1", "contains"),
            QueryFilter("Field2", "value2", "contains"),
        ]
        args = list(self.args) + [view_name, filter_array]
        # Expected query field values in post request body
        query_field = {
            "query.Field1~eq": ["value"],
            "query.Field2~contains": ["value1", "value2"],
        }
        # Update post request body with expected query field values
        self.expected_kwargs["data"].update(query_field)

        success_test(
            test,
            self.service.get_successful_response(),
            select_rows,
            True,
            *args,
            **self.expected_kwargs,
        )

    def test_unauthorized(self):
        test = self
        throws_error_test(
            test,
            RequestAuthorizationError,
            self.service.get_unauthorized_response(),
            select_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_not_found(self):
        test = self
        throws_error_test(
            test,
            QueryNotFoundError,
            self.service.get_query_not_found_response(),
            select_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_server_not_found(self):
        test = self
        throws_error_test(
            test,
            ServerNotFoundError,
            self.service.get_server_not_found_response(),
            select_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_general_error(self):
        test = self
        throws_error_test(
            test,
            RequestError,
            self.service.get_general_error_response(),
            select_rows,
            *self.args,
            **self.expected_kwargs,
        )


class TestSaveRows(unittest.TestCase):
    def setUp(self):
        self.service = MockSaveRows()
        commands = [
            {
                "command": "insert",
                "schema_name": "exp",
                "query_name": "materials",
                "rows": [{"name": "New Sample 1"}],
            }
        ]

        expected_payload = {
            "commands": [
                {
                    "command": "insert",
                    "schemaName": "exp",
                    "queryName": "materials",
                    "rows": [{"name": "New Sample 1"}],
                }
            ]
        }

        self.expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": json.dumps(expected_payload, sort_keys=True),
            "headers": {"Content-Type": "application/json"},
            "timeout": 300,
            "allow_redirects": False,
        }

        self.args = [mock_server_context(self.service), commands]

    def test_success(self):
        test = self
        success_test(
            test,
            self.service.get_successful_response(),
            save_rows,
            True,
            *self.args,
            **self.expected_kwargs,
        )

    def test_unauthorized(self):
        test = self
        throws_error_test(
            test,
            RequestAuthorizationError,
            self.service.get_unauthorized_response(),
            save_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_query_not_found(self):
        test = self
        throws_error_test(
            test,
            QueryNotFoundError,
            self.service.get_query_not_found_response(),
            save_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_server_not_found(self):
        test = self
        throws_error_test(
            test,
            ServerNotFoundError,
            self.service.get_server_not_found_response(),
            save_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_general_error(self):
        test = self
        throws_error_test(
            test,
            RequestError,
            self.service.get_general_error_response(),
            save_rows,
            *self.args,
            **self.expected_kwargs,
        )

    def test_with_optional_command_fields(self):
        """Test save_rows with all optional fields populated in command"""
        commands = [
            {
                "command": "update",
                "schema_name": "exp",
                "query_name": "materials",
                "rows": [{"rowId": 1, "name": "Updated Sample"}],
                "audit_behavior": "DETAILED",
                "audit_user_comment": "Test update comment",
                "container_path": "/custom/path",
                "extra_context": {"custom": "data"},
                "skip_reselect_rows": True,
            }
        ]

        expected_payload = {
            "commands": [
                {
                    "command": "update",
                    "schemaName": "exp",
                    "queryName": "materials",
                    "rows": [{"rowId": 1, "name": "Updated Sample"}],
                    "auditBehavior": "DETAILED",
                    "auditUserComment": "Test update comment",
                    "containerPath": "/custom/path",
                    "extraContext": {"custom": "data"},
                    "skipReselectRows": True,
                }
            ]
        }

        expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": json.dumps(expected_payload, sort_keys=True),
            "headers": {"Content-Type": "application/json"},
            "timeout": 300,
            "allow_redirects": False,
        }

        args = [mock_server_context(self.service), commands]

        success_test(
            self, self.service.get_successful_response(), save_rows, True, *args, **expected_kwargs
        )

    def test_with_optional_parameters(self):
        api_version = 18.21
        commands = [
            {
                "command": "delete",
                "schema_name": "exp",
                "query_name": "materials",
                "rows": [{"rowId": 1}],
            }
        ]
        extra_context = {"global": "context"}
        transacted = False
        timeout = 600
        validate_only = True

        expected_payload = {
            "commands": [
                {
                    "command": "delete",
                    "schemaName": "exp",
                    "queryName": "materials",
                    "rows": [{"rowId": 1}],
                }
            ],
            "apiVersion": api_version,
            "extraContext": extra_context,
            "transacted": transacted,
            "validateOnly": True,
        }

        expected_kwargs = {
            "expected_args": [self.service.get_server_url()],
            "data": json.dumps(expected_payload, sort_keys=True),
            "headers": {"Content-Type": "application/json"},
            "timeout": timeout,
            "allow_redirects": False,
        }

        args = [
            mock_server_context(self.service),
            commands,
            api_version,
            None,  # container_path
            extra_context,
            timeout,
            transacted,
            validate_only,
        ]

        success_test(
            self, self.service.get_successful_response(), save_rows, True, *args, **expected_kwargs
        )


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite(
        [
            load_tests(TestDeleteRows),
            load_tests(TestUpdateRows),
            load_tests(TestInsertRows),
            load_tests(TestExecuteSQL),
            load_tests(TestSelectRows),
            load_tests(TestSaveRows),
        ]
    )


if __name__ == "__main__":
    unittest.main()
