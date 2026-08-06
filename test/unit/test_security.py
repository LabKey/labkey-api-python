#
# Copyright (c) 2017-2026 LabKey Corporation
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
import pytest

from labkey.security import (
    create_user,
    reset_password,
    activate_users,
    deactivate_users,
    delete_users,
    add_to_group,
    remove_from_group,
    remove_from_role,
    add_to_role,
    get_roles,
    list_groups,
)
from labkey.exceptions import (
    RequestError,
    QueryNotFoundError,
    ServerNotFoundError,
    RequestAuthorizationError,
)

from .utilities import MockLabKey, mock_server_context, success_test, throws_error_test


class MockSecurityController(MockLabKey):
    default_action = "security"
    default_success_body = {"success": True}
    use_ssl = False


class MockUserController(MockLabKey):
    default_action = "user"
    default_success_body = {"success": True, "status_code": 200}
    use_ssl = False


@pytest.fixture
def create_user_setup():
    email = "pyTest@labkey.com"

    class MockCreateUser(MockSecurityController):
        api = "createNewUser.api"

    service = MockCreateUser()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"email": email, "sendEmail": False},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), email]
    return service, args, expected_kwargs


def test_create_user_success(create_user_setup):
    service, args, expected_kwargs = create_user_setup
    success_test(service.get_successful_response(), create_user, True, *args, **expected_kwargs)


def test_create_user_unauthorized(create_user_setup):
    service, args, expected_kwargs = create_user_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        create_user,
        *args,
        **expected_kwargs,
    )


def test_create_user_query_not_found(create_user_setup):
    service, args, expected_kwargs = create_user_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        create_user,
        *args,
        **expected_kwargs,
    )


def test_create_user_server_not_found(create_user_setup):
    service, args, expected_kwargs = create_user_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        create_user,
        *args,
        **expected_kwargs,
    )


def test_create_user_general_error(create_user_setup):
    service, args, expected_kwargs = create_user_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), create_user, *args, **expected_kwargs
    )


@pytest.fixture
def reset_password_setup():
    email = "pyTest@labkey.com"

    class MockResetPassword(MockSecurityController):
        api = "adminRotatePassword.api"

    service = MockResetPassword()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"email": email},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), email]
    return service, args, expected_kwargs


def test_reset_password_success(reset_password_setup):
    service, args, expected_kwargs = reset_password_setup
    success_test(service.get_successful_response(), reset_password, True, *args, **expected_kwargs)


def test_reset_password_unauthorized(reset_password_setup):
    service, args, expected_kwargs = reset_password_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        reset_password,
        *args,
        **expected_kwargs,
    )


def test_reset_password_query_not_found(reset_password_setup):
    service, args, expected_kwargs = reset_password_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        reset_password,
        *args,
        **expected_kwargs,
    )


def test_reset_password_server_not_found(reset_password_setup):
    service, args, expected_kwargs = reset_password_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        reset_password,
        *args,
        **expected_kwargs,
    )


def test_reset_password_general_error(reset_password_setup):
    service, args, expected_kwargs = reset_password_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), reset_password, *args, **expected_kwargs
    )


@pytest.fixture
def activate_users_setup():
    user_ids = [123]

    class MockActivateUser(MockUserController):
        api = "activateUsers.api"

    service = MockActivateUser()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"userId": user_ids},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), user_ids]
    return service, args, expected_kwargs


def test_activate_users_success(activate_users_setup):
    service, args, expected_kwargs = activate_users_setup
    success_test(service.get_successful_response(), activate_users, True, *args, **expected_kwargs)


def test_activate_users_unauthorized(activate_users_setup):
    service, args, expected_kwargs = activate_users_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        activate_users,
        *args,
        **expected_kwargs,
    )


def test_activate_users_query_not_found(activate_users_setup):
    service, args, expected_kwargs = activate_users_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        activate_users,
        *args,
        **expected_kwargs,
    )


def test_activate_users_server_not_found(activate_users_setup):
    service, args, expected_kwargs = activate_users_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        activate_users,
        *args,
        **expected_kwargs,
    )


def test_activate_users_general_error(activate_users_setup):
    service, args, expected_kwargs = activate_users_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), activate_users, *args, **expected_kwargs
    )


@pytest.fixture
def deactivate_users_setup():
    user_ids = [123]

    class MockDeactivateUser(MockUserController):
        api = "deactivateUsers.view"

    service = MockDeactivateUser()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"userId": user_ids},
        "headers": None,
        "timeout": 300,
        "allow_redirects": True,
    }
    args = [mock_server_context(service), user_ids]
    return service, args, expected_kwargs


def test_deactivate_users_success(deactivate_users_setup):
    service, args, expected_kwargs = deactivate_users_setup
    success_test(
        service.get_successful_response(), deactivate_users, False, *args, **expected_kwargs
    )


def test_deactivate_users_unauthorized(deactivate_users_setup):
    service, args, expected_kwargs = deactivate_users_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        deactivate_users,
        *args,
        **expected_kwargs,
    )


def test_deactivate_users_query_not_found(deactivate_users_setup):
    service, args, expected_kwargs = deactivate_users_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        deactivate_users,
        *args,
        **expected_kwargs,
    )


def test_deactivate_users_server_not_found(deactivate_users_setup):
    service, args, expected_kwargs = deactivate_users_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        deactivate_users,
        *args,
        **expected_kwargs,
    )


def test_deactivate_users_general_error(deactivate_users_setup):
    service, args, expected_kwargs = deactivate_users_setup
    throws_error_test(
        RequestError,
        service.get_general_error_response(),
        deactivate_users,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def delete_users_setup():
    user_ids = [123]

    class MockDeleteUser(MockUserController):
        api = "deleteUsers.view"

    service = MockDeleteUser()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"userId": user_ids},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), user_ids]
    return service, args, expected_kwargs


def test_delete_users_success(delete_users_setup):
    service, args, expected_kwargs = delete_users_setup
    success_test(service.get_successful_response(), delete_users, False, *args, **expected_kwargs)


def test_delete_users_unauthorized(delete_users_setup):
    service, args, expected_kwargs = delete_users_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        delete_users,
        *args,
        **expected_kwargs,
    )


def test_delete_users_query_not_found(delete_users_setup):
    service, args, expected_kwargs = delete_users_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        delete_users,
        *args,
        **expected_kwargs,
    )


def test_delete_users_server_not_found(delete_users_setup):
    service, args, expected_kwargs = delete_users_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        delete_users,
        *args,
        **expected_kwargs,
    )


def test_delete_users_general_error(delete_users_setup):
    service, args, expected_kwargs = delete_users_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), delete_users, *args, **expected_kwargs
    )


@pytest.fixture
def add_to_group_setup():
    user_id = 321
    group_id = 123

    class MockAddGroupMember(MockSecurityController):
        api = "addGroupMember.api"

    service = MockAddGroupMember()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"groupId": 123, "principalIds": [321]},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), user_id, group_id]
    return service, args, expected_kwargs


def test_add_to_group_success(add_to_group_setup):
    service, args, expected_kwargs = add_to_group_setup
    success_test(service.get_successful_response(), add_to_group, False, *args, **expected_kwargs)


def test_add_to_group_unauthorized(add_to_group_setup):
    service, args, expected_kwargs = add_to_group_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        add_to_group,
        *args,
        **expected_kwargs,
    )


def test_add_to_group_query_not_found(add_to_group_setup):
    service, args, expected_kwargs = add_to_group_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        add_to_group,
        *args,
        **expected_kwargs,
    )


def test_add_to_group_server_not_found(add_to_group_setup):
    service, args, expected_kwargs = add_to_group_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        add_to_group,
        *args,
        **expected_kwargs,
    )


def test_add_to_group_general_error(add_to_group_setup):
    service, args, expected_kwargs = add_to_group_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), add_to_group, *args, **expected_kwargs
    )


@pytest.fixture
def remove_from_group_setup():
    user_id = 321
    group_id = 123

    class MockRemoveGroupMember(MockSecurityController):
        api = "removeGroupMember.api"

    service = MockRemoveGroupMember()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"groupId": 123, "principalIds": [321]},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), user_id, group_id]
    return service, args, expected_kwargs


def test_remove_from_group_success(remove_from_group_setup):
    service, args, expected_kwargs = remove_from_group_setup
    success_test(
        service.get_successful_response(), remove_from_group, False, *args, **expected_kwargs
    )


def test_remove_from_group_unauthorized(remove_from_group_setup):
    service, args, expected_kwargs = remove_from_group_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        remove_from_group,
        *args,
        **expected_kwargs,
    )


def test_remove_from_group_query_not_found(remove_from_group_setup):
    service, args, expected_kwargs = remove_from_group_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        remove_from_group,
        *args,
        **expected_kwargs,
    )


def test_remove_from_group_server_not_found(remove_from_group_setup):
    service, args, expected_kwargs = remove_from_group_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        remove_from_group,
        *args,
        **expected_kwargs,
    )


def test_remove_from_group_general_error(remove_from_group_setup):
    service, args, expected_kwargs = remove_from_group_setup
    throws_error_test(
        RequestError,
        service.get_general_error_response(),
        remove_from_group,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def remove_from_role_setup():
    user_id = 321
    email = "pyTest@labkey.com"
    role = {"uniqueName": "TestRole"}

    class MockRemoveRole(MockSecurityController):
        api = "removeAssignment.api"

    service = MockRemoveRole()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {
            "roleClassName": "TestRole",
            "principalId": 321,
            "email": "pyTest@labkey.com",
        },
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), role, user_id, email]
    return service, args, expected_kwargs


def test_remove_from_role_success(remove_from_role_setup):
    service, args, expected_kwargs = remove_from_role_setup
    success_test(
        service.get_successful_response(), remove_from_role, False, *args, **expected_kwargs
    )


def test_remove_from_role_unauthorized(remove_from_role_setup):
    service, args, expected_kwargs = remove_from_role_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        remove_from_role,
        *args,
        **expected_kwargs,
    )


def test_remove_from_role_query_not_found(remove_from_role_setup):
    service, args, expected_kwargs = remove_from_role_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        remove_from_role,
        *args,
        **expected_kwargs,
    )


def test_remove_from_role_server_not_found(remove_from_role_setup):
    service, args, expected_kwargs = remove_from_role_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        remove_from_role,
        *args,
        **expected_kwargs,
    )


def test_remove_from_role_general_error(remove_from_role_setup):
    service, args, expected_kwargs = remove_from_role_setup
    throws_error_test(
        RequestError,
        service.get_general_error_response(),
        remove_from_role,
        *args,
        **expected_kwargs,
    )


@pytest.fixture
def add_to_role_setup():
    user_id = 321
    email = "pyTest@labkey.com"
    role = {"uniqueName": "TestRole"}

    class MockAddRole(MockSecurityController):
        api = "addAssignment.api"

    service = MockAddRole()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {
            "roleClassName": "TestRole",
            "principalId": 321,
            "email": "pyTest@labkey.com",
        },
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), role, user_id, email]
    return service, args, expected_kwargs


def test_add_to_role_success(add_to_role_setup):
    service, args, expected_kwargs = add_to_role_setup
    success_test(service.get_successful_response(), add_to_role, False, *args, **expected_kwargs)


def test_add_to_role_unauthorized(add_to_role_setup):
    service, args, expected_kwargs = add_to_role_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        add_to_role,
        *args,
        **expected_kwargs,
    )


def test_add_to_role_query_not_found(add_to_role_setup):
    service, args, expected_kwargs = add_to_role_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        add_to_role,
        *args,
        **expected_kwargs,
    )


def test_add_to_role_server_not_found(add_to_role_setup):
    service, args, expected_kwargs = add_to_role_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        add_to_role,
        *args,
        **expected_kwargs,
    )


def test_add_to_role_general_error(add_to_role_setup):
    service, args, expected_kwargs = add_to_role_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), add_to_role, *args, **expected_kwargs
    )


@pytest.fixture
def get_roles_setup():
    class MockGetRoles(MockSecurityController):
        api = "getRoles.api"

    service = MockGetRoles()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": None,
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service)]
    return service, args, expected_kwargs


def test_get_roles_success(get_roles_setup):
    service, args, expected_kwargs = get_roles_setup
    success_test(service.get_successful_response(), get_roles, False, *args, **expected_kwargs)


def test_get_roles_unauthorized(get_roles_setup):
    service, args, expected_kwargs = get_roles_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        get_roles,
        *args,
        **expected_kwargs,
    )


def test_get_roles_query_not_found(get_roles_setup):
    service, args, expected_kwargs = get_roles_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        get_roles,
        *args,
        **expected_kwargs,
    )


def test_get_roles_server_not_found(get_roles_setup):
    service, args, expected_kwargs = get_roles_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        get_roles,
        *args,
        **expected_kwargs,
    )


def test_get_roles_general_error(get_roles_setup):
    service, args, expected_kwargs = get_roles_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), get_roles, *args, **expected_kwargs
    )


@pytest.fixture
def list_groups_setup():
    class MockListGroups(MockSecurityController):
        api = "listProjectGroups.api"

    service = MockListGroups()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": {"includeSiteGroups": True},
        "headers": None,
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), True]
    return service, args, expected_kwargs


def test_list_groups_success(list_groups_setup):
    service, args, expected_kwargs = list_groups_setup
    success_test(service.get_successful_response(), list_groups, False, *args, **expected_kwargs)


def test_list_groups_unauthorized(list_groups_setup):
    service, args, expected_kwargs = list_groups_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        list_groups,
        *args,
        **expected_kwargs,
    )


def test_list_groups_query_not_found(list_groups_setup):
    service, args, expected_kwargs = list_groups_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        list_groups,
        *args,
        **expected_kwargs,
    )


def test_list_groups_server_not_found(list_groups_setup):
    service, args, expected_kwargs = list_groups_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        list_groups,
        *args,
        **expected_kwargs,
    )


def test_list_groups_general_error(list_groups_setup):
    service, args, expected_kwargs = list_groups_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), list_groups, *args, **expected_kwargs
    )
