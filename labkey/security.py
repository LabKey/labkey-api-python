#
# Copyright (c) 2017-2018 LabKey Corporation
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
import functools
from dataclasses import dataclass

from typing import Union, List

from labkey.server_context import ServerContext

SECURITY_CONTROLLER = "security"
USER_CONTROLLER = "user"
LOGIN_CONTROLLER = "login"


def activate_users(
    server_context: ServerContext, target_ids: List[int], container_path: str = None
):
    """
    Activate user accounts
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param target_ids:
    :param container_path:
    :return:
    """
    return __make_user_api_request(
        server_context,
        target_ids=target_ids,
        api="activateUsers.api",
        container_path=container_path,
    )


def add_to_group(
    server_context: ServerContext,
    user_ids: Union[int, List[int]],
    group_id: int,
    container_path: str = None,
):
    """
    Add user to group
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param user_ids: users to add
    :param group_id: to add to
    :param container_path:
    :return:
    """
    return __make_security_group_api_request(
        server_context, "addGroupMember.api", user_ids, group_id, container_path
    )


def add_to_role(
    server_context: ServerContext,
    role: dict,
    user_id: int = None,
    email: str = None,
    container_path: str = None,
):
    """
    Add user/group to security role
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param role: (from get_roles) to add user to
    :param user_id: to add permissions role to (must supply this or email or both)
    :param email: to add permissions role to (must supply this or user_id or both)
    :param container_path: additional project path context
    :return:
    """
    return __make_security_role_api_request(
        server_context,
        "addAssignment.api",
        role,
        user_id=user_id,
        email=email,
        container_path=container_path,
    )


def create_user(
    server_context: ServerContext, email: str, container_path: str = None, send_email=False
):
    """
    Create new account
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param email:
    :param container_path:
    :param send_email: true to send email notification to user
    :return:
    """
    url = server_context.build_url(SECURITY_CONTROLLER, "createNewUser.api", container_path)
    payload = {"email": email, "sendEmail": send_email}

    return server_context.make_request(url, payload)


def deactivate_users(
    server_context: ServerContext, target_ids: List[int], container_path: str = None
) -> dict:
    """
    Deactivate but do not delete user accounts
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param target_ids:
    :param container_path:
    :return:
    """
    # This action responds with HTML so we just check if it responds OK
    response = __make_user_api_request(
        server_context,
        target_ids=target_ids,
        api="deactivateUsers.view",
        container_path=container_path,
    )
    if response is not None and response["status_code"] == 200:
        return dict(success=True)
    else:
        raise ValueError("Unable to deactivate users {0}".format(target_ids))


def delete_users(server_context: ServerContext, target_ids: List[int], container_path: str = None):
    """
    Delete user accounts
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param target_ids:
    :param container_path:
    :return:
    """
    # This action responds with HTML so we just check if it responds OK
    response = __make_user_api_request(
        server_context,
        target_ids=target_ids,
        api="deleteUsers.view",
        container_path=container_path,
    )
    if response is not None and response["status_code"] == 200:
        return dict(success=True)
    else:
        raise ValueError("Unable to delete users {0}".format(target_ids))


def get_roles(server_context: ServerContext, container_path: str = None):
    """
    Gets the set of permissions and roles available from the server
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param container_path:
    :return:
    """
    url = server_context.build_url(
        SECURITY_CONTROLLER, "getRoles.api", container_path=container_path
    )
    return server_context.make_request(url)


def get_user_by_email(server_context: ServerContext, email: str):
    """
    Get the user with the provided email. Throws a ValueError if not found.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param email:
    :return:
    """
    url = server_context.build_url(USER_CONTROLLER, "getUsers.api")
    payload = {"includeDeactivatedAccounts": True}
    result = server_context.make_request(url, payload)

    if result is None or result["users"] is None:
        raise ValueError("No Users in container" + email)

    for user in result["users"]:
        if user["email"] == email:
            return user
    else:
        raise ValueError("User not found: " + email)


def list_groups(
    server_context: ServerContext, include_site_groups: bool = False, container_path: str = None
):
    url = server_context.build_url(SECURITY_CONTROLLER, "listProjectGroups.api", container_path)
    return server_context.make_request(url, {"includeSiteGroups": include_site_groups})


def remove_from_group(
    server_context: ServerContext,
    user_ids: Union[int, List[int]],
    group_id,
    container_path: str = None,
):
    """
    Remove user from group
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param user_ids:
    :param group_id:
    :param container_path:
    :return:
    """
    return __make_security_group_api_request(
        server_context, "removeGroupMember.api", user_ids, group_id, container_path
    )


def remove_from_role(
    server_context: ServerContext,
    role: dict,
    user_id: int = None,
    email: str = None,
    container_path: str = None,
):
    """
    Remove user/group from security role
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param role: (from get_roles) to remove user from
    :param user_id: to remove permissions from (must supply this or email or both)
    :param email: to remove permissions from (must supply this or user_id or both)
    :param container_path: additional project path context
    :return:
    """
    return __make_security_role_api_request(
        server_context,
        "removeAssignment.api",
        role,
        user_id=user_id,
        email=email,
        container_path=container_path,
    )


def reset_password(server_context: ServerContext, email: str, container_path: str = None):
    """
    Change password for a user  (Requires Admin privileges on the LabKey server)
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param email:
    :param container_path:
    :return:
    """
    url = server_context.build_url(SECURITY_CONTROLLER, "adminRotatePassword.api", container_path)
    return server_context.make_request(url, {"email": email})


def impersonate_user(
    server_context: ServerContext,
    user_id: int = None,
    email: str = None,
    container_path: str = None,
):
    """
    For site-admins or project-admins only, start impersonating a user.

    Admins may impersonate other users to perform actions on their behalf.
    Site users may impersonate any user in any project. Project admins must
    execute this command in a project in which they have admin permission
    and may impersonate any user that has access to the project.

    To finish an impersonation session use `stop_impersonating`.

    :param user_id: to impersonate (must supply this or email)
    :param email: to impersonate (must supply this or user_id)
    :param container_path: in which to impersonate the user
    """
    if email is None and user_id is None:
        raise ValueError("Must supply either [email] or [user_id]")

    url = server_context.build_url(USER_CONTROLLER, "impersonateUser.api", container_path)
    return server_context.make_request(url, {"userId": user_id, "email": email})


def stop_impersonating(server_context: ServerContext):
    """
    Stop impersonating a user while keeping the original user logged in.
    """
    url = server_context.build_url(LOGIN_CONTROLLER, "stopImpersonating.api")
    return server_context.make_request(url)


@dataclass
class WhoAmI:
    id: int
    email: str
    display_name: str
    impersonated: str
    CSRF: str


def who_am_i(server_context: ServerContext) -> WhoAmI:
    """
    Calls the whoami API and returns a WhoAmI object.
    """
    url = server_context.build_url("login", "whoami.api")
    response = server_context.make_request(url)
    return WhoAmI(
        response["id"],
        response["email"],
        response["displayName"],
        response["impersonated"],
        response["CSRF"],
    )


def __make_security_group_api_request(
    server_context: ServerContext,
    api: str,
    user_ids: Union[int, List[int]],
    group_id: int,
    container_path: str = None,
):
    """
    Execute a request against the LabKey Security Controller Group Membership apis
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param api: Action to execute
    :param user_ids: user ids to apply action to
    :param group_id: group id to apply action to
    :param container_path: Additional container context path
    :return: Request json object
    """
    url = server_context.build_url(SECURITY_CONTROLLER, api, container_path)

    # if user_ids is only a single scalar make it an array
    if not hasattr(user_ids, "__iter__"):
        user_ids = [user_ids]

    return server_context.make_request(url, {"groupId": group_id, "principalIds": user_ids})


def __make_security_role_api_request(
    server_context: ServerContext,
    api: str,
    role: dict,
    email: str = None,
    user_id: int = None,
    container_path: str = None,
):
    """
    Execute a request against the LabKey Security Controller Group Membership apis
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param api: Action to execute
    :param user_id: user ids to apply action to
    :param role: (from get_roles) to remove user from
    :param container_path: Additional container context path
    :return: Request json object
    """
    if email is None and user_id is None:
        raise ValueError("Must supply either/both [email] or [user_id]")

    url = server_context.build_url(SECURITY_CONTROLLER, api, container_path)

    return server_context.make_request(
        url,
        {"roleClassName": role["uniqueName"], "principalId": user_id, "email": email},
    )


def __make_user_api_request(
    server_context: ServerContext, target_ids: List[int], api: str, container_path: str = None
):
    """
    Make a request to the LabKey User Controller
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param target_ids: Array of User ids to affect
    :param api: action to take
    :param container_path: container context
    :return: response json
    """
    url = server_context.build_url(USER_CONTROLLER, api, container_path)

    return server_context.make_request(url, {"userId": target_ids})


class SecurityWrapper:
    """
    Wrapper for all of the API methods exposed in the security module. Used by the APIWrapper class.
    """

    def __init__(self, server_context: ServerContext):
        self.server_context = server_context

    @functools.wraps(activate_users)
    def activate_users(self, target_ids: List[int], container_path: str = None):
        return activate_users(self.server_context, target_ids, container_path)

    @functools.wraps(add_to_group)
    def add_to_group(
        self, user_ids: Union[int, List[int]], group_id: int, container_path: str = None
    ):
        return add_to_group(self.server_context, user_ids, group_id, container_path)

    @functools.wraps(add_to_role)
    def add_to_role(
        self, role: dict, user_id: int = None, email: str = None, container_path: str = None
    ):
        return add_to_role(self.server_context, role, user_id, email, container_path)

    @functools.wraps(create_user)
    def create_user(self, email: str, container_path: str = None, send_email=False):
        return create_user(self.server_context, email, container_path, send_email)

    @functools.wraps(deactivate_users)
    def deactivate_users(self, target_ids: List[int], container_path: str = None):
        return deactivate_users(self.server_context, target_ids, container_path)

    @functools.wraps(delete_users)
    def delete_users(self, target_ids: List[int], container_path: str = None):
        return delete_users(self.server_context, target_ids, container_path)

    @functools.wraps(get_roles)
    def get_roles(self, container_path: str = None):
        return get_roles(self.server_context, container_path)

    @functools.wraps(get_user_by_email)
    def get_user_by_email(self, email: str):
        return get_user_by_email(self.server_context, email)

    @functools.wraps(list_groups)
    def list_groups(self, include_site_groups: bool = False, container_path: str = None):
        return list_groups(self.server_context, include_site_groups, container_path)

    @functools.wraps(remove_from_group)
    def remove_from_group(
        self, user_ids: Union[int, List[int]], group_id, container_path: str = None
    ):
        return remove_from_group(self.server_context, user_ids, group_id, container_path)

    @functools.wraps(remove_from_role)
    def remove_from_role(
        self, role: dict, user_id: int = None, email: str = None, container_path: str = None
    ):
        return remove_from_role(self.server_context, role, user_id, email, container_path)

    @functools.wraps(reset_password)
    def reset_password(self, email: str, container_path: str = None):
        return reset_password(self.server_context, email, container_path)

    @functools.wraps(impersonate_user)
    def impersonate_user(self, user_id: int = None, email: str = None, container_path: str = None):
        return impersonate_user(self.server_context, user_id, email, container_path)

    @functools.wraps(stop_impersonating)
    def stop_impersonating(self):
        return stop_impersonating(self.server_context)

    @functools.wraps(who_am_i)
    def who_am_i(self):
        return who_am_i(self.server_context)
