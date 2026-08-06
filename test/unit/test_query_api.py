#
# Copyright (c) 2015-2026 LabKey Corporation
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
import pytest

from labkey.query import (
    delete_rows,
    update_rows,
    insert_rows,
    save_rows,
    select_rows,
    execute_sql,
    get_queries,
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


class MockGetQueries(MockLabKey):
    api = "getQueries.api"


schema = "testSchema"
query = "testQuery"


@pytest.fixture
def delete_rows_setup():
    service = MockDeleteRows()
    rows = "{id:1234}"
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
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
    args = [mock_server_context(service), schema, query, rows]
    return service, args, expected_kwargs


def test_delete_rows_success(delete_rows_setup):
    service, args, expected_kwargs = delete_rows_setup
    success_test(service.get_successful_response(), delete_rows, True, *args, **expected_kwargs)


def test_delete_rows_unauthorized(delete_rows_setup):
    service, args, expected_kwargs = delete_rows_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        delete_rows,
        *args,
        **expected_kwargs,
    )


def test_delete_rows_query_not_found(delete_rows_setup):
    service, args, expected_kwargs = delete_rows_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        delete_rows,
        *args,
        **expected_kwargs,
    )


def test_delete_rows_server_not_found(delete_rows_setup):
    service, args, expected_kwargs = delete_rows_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        delete_rows,
        *args,
        **expected_kwargs,
    )


def test_delete_rows_general_error(delete_rows_setup):
    service, args, expected_kwargs = delete_rows_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), delete_rows, *args, **expected_kwargs
    )


@pytest.fixture
def update_rows_setup():
    service = MockUpdateRows()
    rows = "{id:1234}"
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
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
    args = [mock_server_context(service), schema, query, rows]
    return service, args, expected_kwargs


def test_update_rows_success(update_rows_setup):
    service, args, expected_kwargs = update_rows_setup
    success_test(service.get_successful_response(), update_rows, True, *args, **expected_kwargs)


def test_update_rows_unauthorized(update_rows_setup):
    service, args, expected_kwargs = update_rows_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        update_rows,
        *args,
        **expected_kwargs,
    )


def test_update_rows_query_not_found(update_rows_setup):
    service, args, expected_kwargs = update_rows_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        update_rows,
        *args,
        **expected_kwargs,
    )


def test_update_rows_server_not_found(update_rows_setup):
    service, args, expected_kwargs = update_rows_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        update_rows,
        *args,
        **expected_kwargs,
    )


def test_update_rows_general_error(update_rows_setup):
    service, args, expected_kwargs = update_rows_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), update_rows, *args, **expected_kwargs
    )


@pytest.fixture
def insert_rows_setup():
    service = MockInsertRows()
    rows = "{id:1234}"
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
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
    args = [mock_server_context(service), schema, query, rows]
    return service, args, expected_kwargs


def test_insert_rows_success(insert_rows_setup):
    service, args, expected_kwargs = insert_rows_setup
    success_test(service.get_successful_response(), insert_rows, True, *args, **expected_kwargs)


def test_insert_rows_unauthorized(insert_rows_setup):
    service, args, expected_kwargs = insert_rows_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        insert_rows,
        *args,
        **expected_kwargs,
    )


def test_insert_rows_query_not_found(insert_rows_setup):
    service, args, expected_kwargs = insert_rows_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        insert_rows,
        *args,
        **expected_kwargs,
    )


def test_insert_rows_server_not_found(insert_rows_setup):
    service, args, expected_kwargs = insert_rows_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        insert_rows,
        *args,
        **expected_kwargs,
    )


def test_insert_rows_general_error(insert_rows_setup):
    service, args, expected_kwargs = insert_rows_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), insert_rows, *args, **expected_kwargs
    )


@pytest.fixture
def execute_sql_setup():
    service = MockExecuteSQL()
    sql = "select * from " + schema + "." + query
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"sql": waf_encode(sql), "schemaName": schema},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema, sql]
    return service, args, expected_kwargs


def test_execute_sql_success(execute_sql_setup):
    service, args, expected_kwargs = execute_sql_setup
    success_test(service.get_successful_response(), execute_sql, True, *args, **expected_kwargs)


def test_execute_sql_unauthorized(execute_sql_setup):
    service, args, expected_kwargs = execute_sql_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        execute_sql,
        *args,
        **expected_kwargs,
    )


def test_execute_sql_query_not_found(execute_sql_setup):
    service, args, expected_kwargs = execute_sql_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        execute_sql,
        *args,
        **expected_kwargs,
    )


def test_execute_sql_server_not_found(execute_sql_setup):
    service, args, expected_kwargs = execute_sql_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        execute_sql,
        *args,
        **expected_kwargs,
    )


def test_execute_sql_general_error(execute_sql_setup):
    service, args, expected_kwargs = execute_sql_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), execute_sql, *args, **expected_kwargs
    )


@pytest.fixture
def select_rows_setup():
    service = MockSelectRows()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"schemaName": schema, "query.queryName": query, "query.maxRows": -1},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema, query]
    return service, args, expected_kwargs


def test_select_rows_success(select_rows_setup):
    service, args, expected_kwargs = select_rows_setup
    success_test(service.get_successful_response(), select_rows, True, *args, **expected_kwargs)


def test_select_rows_query_filter(select_rows_setup):
    service, args, expected_kwargs = select_rows_setup
    view_name = None
    filter_array = [
        QueryFilter("Field1", "value", "eq"),
        QueryFilter("Field2", "value1", "contains"),
        QueryFilter("Field2", "value2", "contains"),
    ]
    test_args = list(args) + [view_name, filter_array]
    # Expected query field values in post request body
    query_field = {
        "query.Field1~eq": ["value"],
        "query.Field2~contains": ["value1", "value2"],
    }
    # Update post request body with expected query field values
    expected_kwargs["data"].update(query_field)

    success_test(
        service.get_successful_response(),
        select_rows,
        True,
        *test_args,
        **expected_kwargs,
    )


def test_select_rows_unauthorized(select_rows_setup):
    service, args, expected_kwargs = select_rows_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        select_rows,
        *args,
        **expected_kwargs,
    )


def test_select_rows_query_not_found(select_rows_setup):
    service, args, expected_kwargs = select_rows_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        select_rows,
        *args,
        **expected_kwargs,
    )


def test_select_rows_server_not_found(select_rows_setup):
    service, args, expected_kwargs = select_rows_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        select_rows,
        *args,
        **expected_kwargs,
    )


def test_select_rows_general_error(select_rows_setup):
    service, args, expected_kwargs = select_rows_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), select_rows, *args, **expected_kwargs
    )


@pytest.fixture
def save_rows_setup():
    service = MockSaveRows()
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

    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": json.dumps(expected_payload, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }

    args = [mock_server_context(service), commands]
    return service, args, expected_kwargs


def test_save_rows_success(save_rows_setup):
    service, args, expected_kwargs = save_rows_setup
    success_test(service.get_successful_response(), save_rows, True, *args, **expected_kwargs)


def test_save_rows_unauthorized(save_rows_setup):
    service, args, expected_kwargs = save_rows_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        save_rows,
        *args,
        **expected_kwargs,
    )


def test_save_rows_query_not_found(save_rows_setup):
    service, args, expected_kwargs = save_rows_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        save_rows,
        *args,
        **expected_kwargs,
    )


def test_save_rows_server_not_found(save_rows_setup):
    service, args, expected_kwargs = save_rows_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        save_rows,
        *args,
        **expected_kwargs,
    )


def test_save_rows_general_error(save_rows_setup):
    service, args, expected_kwargs = save_rows_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), save_rows, *args, **expected_kwargs
    )


def test_save_rows_with_optional_command_fields(save_rows_setup):
    service, _, _ = save_rows_setup
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
        "expected_args": [service.get_server_url()],
        "data": json.dumps(expected_payload, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }

    args = [mock_server_context(service), commands]

    success_test(service.get_successful_response(), save_rows, True, *args, **expected_kwargs)


def test_save_rows_with_optional_parameters(save_rows_setup):
    service, _, _ = save_rows_setup
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
        "expected_args": [service.get_server_url()],
        "data": json.dumps(expected_payload, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": timeout,
        "allow_redirects": False,
    }

    args = [
        mock_server_context(service),
        commands,
        api_version,
        None,  # container_path
        extra_context,
        timeout,
        transacted,
        validate_only,
    ]

    success_test(service.get_successful_response(), save_rows, True, *args, **expected_kwargs)


@pytest.fixture
def get_queries_setup():
    service = MockGetQueries()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"schemaName": schema},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema]
    return service, args, expected_kwargs


def test_get_queries_success(get_queries_setup):
    service, args, expected_kwargs = get_queries_setup
    success_test(service.get_successful_response(), get_queries, True, *args, **expected_kwargs)


def test_get_queries_camel_case(get_queries_setup):
    service, args, expected_kwargs = get_queries_setup
    options = {
        "include_columns": True,
        "include_system_queries": False,
        "include_title": True,
        "include_user_queries": False,
        "include_view_data_url": True,
        "query_detail_columns": False,
    }
    expected_kwargs["data"].update(
        {
            "includeColumns": True,
            "includeSystemQueries": False,
            "includeTitle": True,
            "includeUserQueries": False,
            "includeViewDataUrl": True,
            "queryDetailColumns": False,
        }
    )

    # We use a lambda below because get_queries uses kwargs, but success_test doesn't have a way to pass kwargs
    success_test(
        service.get_successful_response(),
        lambda *a: get_queries(*a, **options),
        True,
        *args,
        **expected_kwargs,
    )
