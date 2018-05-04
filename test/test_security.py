#
# Copyright (c) 2017 LabKey Corporation
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
from labkey.security import create_user, reset_password, activate_users, deactivate_users, delete_users, add_to_group, \
    remove_from_group, remove_from_role, add_to_role, get_roles, list_groups
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError

from test_utils import MockLabKey, mock_server_context, success_test, throws_error_test


class MockSecurityController(MockLabKey):
    default_action = 'security'
    default_success_body = {'success': True}
    use_ssl = False


class MockUserController(MockLabKey):
    default_action = 'user'
    default_success_body = {
        'success': True,
        'status_code': 200
    }
    use_ssl = False


class TestCreateUser(unittest.TestCase):
    __email = 'pyTest@labkey.com'

    class MockCreateUser(MockSecurityController):
        api = 'createNewUser.api'

    def setUp(self):
        self.service = self.MockCreateUser()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'email': TestCreateUser.__email,
                'sendEmail': False
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__email
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), create_user, True, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          create_user, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          create_user, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          create_user, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          create_user, *self.args, **self.expected_kwargs)


class TestResetPassword(unittest.TestCase):
    __email = 'pyTest@labkey.com'

    class MockResetPassword(MockSecurityController):
        api = 'adminRotatePassword.api'

    def setUp(self):
        self.service = self.MockResetPassword()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'email': TestResetPassword.__email
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__email
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), reset_password, True,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          reset_password, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          reset_password, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          reset_password, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          reset_password, *self.args, **self.expected_kwargs)


class TestActivateUsers(unittest.TestCase):
    __user_id = [123]

    class MockActivateUser(MockUserController):
        api = 'activateUsers.api'

    def setUp(self):
        self.service = self.MockActivateUser()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'userId': [123]
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__user_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), activate_users, True,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          activate_users, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          activate_users, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          activate_users, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          activate_users, *self.args, **self.expected_kwargs)


class TestDeactivateUsers(unittest.TestCase):
    __user_id = [123]

    class MockDeactivateUser(MockUserController):
        api = 'deactivateUsers.view'

    def setUp(self):
        self.service = self.MockDeactivateUser()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'userId': [123]
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__user_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), deactivate_users, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          deactivate_users, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          deactivate_users, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          deactivate_users, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          deactivate_users, *self.args, **self.expected_kwargs)


class TestDeleteUsers(unittest.TestCase):
    __user_id = [123]

    class MockDeleteUser(MockUserController):
        api = 'deleteUsers.view'

    def setUp(self):
        self.service = self.MockDeleteUser()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'userId': [123]
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__user_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), delete_users, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          delete_users, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          delete_users, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          delete_users, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          delete_users, *self.args, **self.expected_kwargs)


class TestAddToGroup(unittest.TestCase):
    __user_id = 321
    __group_id = 123

    class MockAddGroupMember(MockSecurityController):
        api = 'addGroupMember.api'

    def setUp(self):
        self.service = self.MockAddGroupMember()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'groupId': 123,
                'principalIds': [321]
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__user_id,
            self.__group_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), add_to_group, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          add_to_group, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          add_to_group, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          add_to_group, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          add_to_group, *self.args, **self.expected_kwargs)


class TestRemoveFromGroup(unittest.TestCase):
    __user_id = 321
    __group_id = 123

    class MockRemoveGroupMember(MockSecurityController):
        api = 'removeGroupMember.api'

    def setUp(self):
        self.service = self.MockRemoveGroupMember()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'groupId': 123,
                'principalIds': [321]
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__user_id,
            self.__group_id
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), remove_from_group, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          remove_from_group, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          remove_from_group, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          remove_from_group, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          remove_from_group, *self.args, **self.expected_kwargs)


class TestRemoveFromRole(unittest.TestCase):
    __user_id = 321
    __email = 'pyTest@labkey.com'
    __role = {'uniqueName': 'TestRole'}

    class MockRemoveRole(MockSecurityController):
        api = 'removeAssignment.api'

    def setUp(self):
        self.service = self.MockRemoveRole()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'roleClassName': 'TestRole',
                'principalId': 321,
                'email': 'pyTest@labkey.com'
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__role,
            self.__user_id,
            self.__email
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), remove_from_role, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          remove_from_role, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          remove_from_role, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          remove_from_role, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          remove_from_role, *self.args, **self.expected_kwargs)


class TestAddToRole(unittest.TestCase):
    __user_id = 321
    __email = 'pyTest@labkey.com'
    __role = {'uniqueName': 'TestRole'}

    class MockAddRole(MockSecurityController):
        api = 'addAssignment.api'

    def setUp(self):
        self.service = self.MockAddRole()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'roleClassName': 'TestRole',
                'principalId': 321,
                'email': 'pyTest@labkey.com'
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            self.__role,
            self.__user_id,
            self.__email
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), add_to_role, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          add_to_role, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          add_to_role, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          add_to_role, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          add_to_role, *self.args, **self.expected_kwargs)


class TestGetRoles(unittest.TestCase):

    class MockGetRoles(MockSecurityController):
        api = 'getRoles.api'

    def setUp(self):
        self.service = self.MockGetRoles()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': None,
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service)
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), get_roles, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          get_roles, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          get_roles, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          get_roles, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          get_roles, *self.args, **self.expected_kwargs)


class TestListGroups(unittest.TestCase):

    class MockListGroups(MockSecurityController):
        api = 'listProjectGroups.api'

    def setUp(self):
        self.service = self.MockListGroups()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': {
                'includeSiteGroups': True
            },
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service),
            True
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), list_groups, False,
                     *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response(),
                          list_groups, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response(),
                          list_groups, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response(),
                          list_groups, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response(),
                          list_groups, *self.args, **self.expected_kwargs)


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite([
        load_tests(TestCreateUser),
        load_tests(TestActivateUsers),
        load_tests(TestDeactivateUsers),
        load_tests(TestDeleteUsers),
        load_tests(TestRemoveFromGroup),
        load_tests(TestAddToGroup),
        load_tests(TestRemoveFromRole)
    ])


if __name__ == '__main__':
    utils.DISABLE_CSRF_CHECK = True
    unittest.main()
