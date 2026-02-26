#
# Copyright (c) 2018 LabKey Corporation
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
import os
import tempfile
import pytest

from labkey.domain import (
    create,
    conditional_format,
    Domain,
    drop,
    encode_conditional_format_filter,
    get,
    infer_fields,
    save,
)
from labkey.exceptions import RequestAuthorizationError
from labkey.query import QueryFilter

from .utilities import (
    MockLabKey,
    mock_server_context,
    success_test,
    success_test_get,
    throws_error_test,
    throws_error_test_get,
)

domain_controller = "property"


@pytest.fixture
def create_setup():
    domain_definition = {
        "kind": "IntList",
        "domainDesign": {
            "name": "TheTestList",
            "fields": [{"name": "theKey", "rangeURI": "int"}],
        },
        "options": {"keyName": "theKey"},
    }

    class MockCreate(MockLabKey):
        api = "createDomain.api"
        default_action = domain_controller
        default_success_body = domain_definition

    service = MockCreate()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": json.dumps(domain_definition, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), domain_definition]
    return service, args, expected_kwargs


def test_create_success(create_setup):
    service, args, expected_kwargs = create_setup
    success_test(service.get_successful_response(), create, False, *args, **expected_kwargs)


def test_create_unauthorized(create_setup):
    service, args, expected_kwargs = create_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        create,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def drop_setup():
    schema_name = "lists"
    query_name = "TheTestList"

    class MockDrop(MockLabKey):
        api = "deleteDomain.api"
        default_action = domain_controller
        default_success_body = {}

    service = MockDrop()
    payload = {"schemaName": schema_name, "queryName": query_name}
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": json.dumps(payload, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema_name, query_name]
    return service, args, expected_kwargs


def test_drop_success(drop_setup):
    service, args, expected_kwargs = drop_setup
    success_test(service.get_successful_response(), drop, False, *args, **expected_kwargs)


def test_drop_unauthorized(drop_setup):
    service, args, expected_kwargs = drop_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        drop,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def get_setup():
    schema_name = "lists"
    query_name = "TheTestList"

    class MockGet(MockLabKey):
        api = "getDomain.api"
        default_action = domain_controller
        default_success_body = {}

    service = MockGet()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "headers": None,
        "params": {"schemaName": schema_name, "queryName": query_name},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema_name, query_name]
    return service, args, expected_kwargs


def test_get_success(get_setup):
    service, args, expected_kwargs = get_setup
    success_test_get(service.get_successful_response(), get, False, *args, **expected_kwargs)


def test_get_unauthorized(get_setup):
    service, args, expected_kwargs = get_setup
    throws_error_test_get(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        get,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def infer_fields_setup():
    class MockInferFields(MockLabKey):
        api = "inferDomain.api"
        default_action = domain_controller
        default_success_body = {}

    service = MockInferFields()
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "w") as tmp:
        tmp.write("Name\tAge\nNick\t32\nBrian\t27\n")

    # Re-open the file for reading in the test
    file = open(path, "r")
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": None,
        "files": {"inferfile": file},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), file]
    yield service, args, expected_kwargs
    file.close()
    os.remove(path)


def test_infer_fields_success(infer_fields_setup):
    service, args, expected_kwargs = infer_fields_setup
    success_test(service.get_successful_response(), infer_fields, False, *args, **expected_kwargs)


def test_infer_fields_unauthorized(infer_fields_setup):
    service, args, expected_kwargs = infer_fields_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        infer_fields,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def save_setup():
    domain = Domain(
        **{
            "container": "TestContainer",
            "description": "A Test Domain",
            "domain_id": 9823,
        }
    )
    schema_name = "lists"
    query_name = "TheTestList"

    class MockSave(MockLabKey):
        api = "saveDomain.api"
        default_action = domain_controller
        default_success_body = {}

    service = MockSave()
    payload = {
        "domainDesign": domain.to_json(),
        "queryName": query_name,
        "schemaName": schema_name,
    }
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": json.dumps(payload, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema_name, query_name, domain]
    return service, args, expected_kwargs


def test_save_success(save_setup):
    service, args, expected_kwargs = save_setup
    success_test(service.get_successful_response(), save, False, *args, **expected_kwargs)


def test_save_unauthorized(save_setup):
    service, args, expected_kwargs = save_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        save,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def conditional_format_create_setup():
    domain_definition = {
        "kind": "IntList",
        "domainDesign": {
            "name": "TheTestList_cf",
            "fields": [
                {
                    "name": "theKey",
                    "rangeURI": "int",
                    "conditionalFormats": [
                        {
                            "filter": encode_conditional_format_filter(QueryFilter("theKey", 500)),
                            "textColor": "f44e3b",
                            "backgroundColor": "fcba03",
                            "bold": True,
                            "italic": True,
                            "strikethrough": False,
                        }
                    ],
                }
            ],
        },
    }

    class MockCreate(MockLabKey):
        api = "createDomain.api"
        default_action = domain_controller
        default_success_body = domain_definition

    service = MockCreate()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": json.dumps(domain_definition, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), domain_definition]
    return service, args, expected_kwargs


def test_conditional_format_create_success(conditional_format_create_setup):
    service, args, expected_kwargs = conditional_format_create_setup
    success_test(service.get_successful_response(), create, False, *args, **expected_kwargs)


def test_conditional_format_create_unauthorized(conditional_format_create_setup):
    service, args, expected_kwargs = conditional_format_create_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        create,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def conditional_format_save_setup():
    schema_name = "lists"
    query_name = "TheTestList_cf"
    test_domain = Domain(
        **{
            "container": "TestContainer",
            "description": "A Test Domain",
            "domain_id": 5314,
            "fields": [{"name": "theKey", "rangeURI": "int"}],
        }
    )
    test_domain.fields[0].conditional_formats = [
        # create conditional format using our utility for a QueryFilter
        conditional_format(
            background_color="fcba03",
            bold=True,
            italic=True,
            query_filter=QueryFilter("theKey", 200),
            strike_through=True,
            text_color="f44e3b",
        ),
        # create conditional format using our utility for a QueryFilter list
        conditional_format(
            background_color="fcba03",
            bold=True,
            italic=True,
            query_filter=[
                QueryFilter("theKey", 500, QueryFilter.Types.GREATER_THAN),
                QueryFilter("theKey", 1000, QueryFilter.Types.LESS_THAN),
            ],
            strike_through=True,
            text_color="f44e3b",
        ),
    ]

    class MockSave(MockLabKey):
        api = "saveDomain.api"
        default_action = domain_controller
        default_success_body = {}

    service = MockSave()
    payload = {
        "domainDesign": test_domain.to_json(),
        "queryName": query_name,
        "schemaName": schema_name,
    }
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": json.dumps(payload, sort_keys=True),
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), schema_name, query_name, test_domain]
    return service, args, expected_kwargs


def test_conditional_format_save_success(conditional_format_save_setup):
    service, args, expected_kwargs = conditional_format_save_setup
    success_test(service.get_successful_response(), save, True, *args, **expected_kwargs)


def test_conditional_format_save_unauthorized(conditional_format_save_setup):
    service, args, expected_kwargs = conditional_format_save_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        save,
        *args,
        **expected_kwargs,
    )
