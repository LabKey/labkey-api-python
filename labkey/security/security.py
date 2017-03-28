

from __future__ import unicode_literals
import json

from requests.exceptions import SSLError
from labkey.utils import build_url, handle_response
from labkey.exceptions import ServerContextError, ServerNotFoundError, RequestError

_default_timeout = 60 * 5  # 5 minutes
security_controller = 'security'
login_controller = 'login'
user_controller = 'user'


def create_user(server_context, email, container_path=None, send_email=False,):
    """
    Create new account (specify username, email and all other fields in user properties)
    :param server_context:
    :param email:
    :param container_path:
    :param send_email: true to send email notification to user
    :param timeout: for request
    :return:
    """
    url = build_url(server_context, security_controller, 'CreateNewUser.api', container_path)
    payload = {
        'email': email,
        'sendEmail': send_email
    }

    return __make_request(server_context, url, payload)


def activate_user(server_context, target_id, container_path=None):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_id:
    :param container_path:
    :return:
    """
    return activate_users(server_context, target_ids=[target_id], container_path=container_path)


def activate_users(server_context, target_ids, container_path=None):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_ids:
    :param container_path:
    :return:
    """
    return __make_user_api_request(server_context, target_ids=target_ids, api='ActivateUsers.api', container_path=container_path)



def deactivate_user(server_context, target_id, container_path=None):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_id:
    :param container_path:
    :return:
    """
    return deactivate_users(server_context, target_ids=[target_id], container_path=container_path)


def deactivate_users(server_context, target_ids, container_path=None):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_ids:
    :param container_path:
    :return:
    """
    return __make_user_api_request(server_context, target_ids=target_ids, api='DeactivateUsers.api', container_path=container_path)


def delete_user(server_context, target_id, container_path=None):
    """
    Delete user account
    :param target_id:
    :param server_context:
    :param container_path:
    :return:
    """
    return delete_users(server_context, target_ids=[target_id], container_path=container_path)


def delete_users(server_context, target_ids, container_path=None):
    """
    Delete user account
    :param target_id:
    :param server_context:
    :param container_path:
    :return:
    """
    return __make_user_api_request(server_context, target_ids=target_ids, api='DeleteUsers.api', container_path=container_path)


def __make_user_api_request(server_context, target_ids, api, container_path=None):
    """
    Make a request to the LabKey User Controller
    :param server_context: to make request to
    :param target_ids: Array of User ids to affect
    :param api: action to take
    :param container_path: container context
    :return: response json
    """
    url = build_url(server_context, user_controller, api, container_path)
    payload = {
        'userId': target_ids
    }

    return __make_request(server_context, url, payload)


def add_to_group(server_context, user_ids, project_group_id, container_path=None):
    """
    Add user to group
    :param server_context: LabKey server context
    :param user_ids: users to add
    :param project_group_id: to add to
    :param container_path:
    :param fail_if_member:
    :return:
    """
    return __make_security_group_api_request(server_context, 'AddGroupMember.api', user_ids, project_group_id, container_path)


def remove_from_group(server_context, user_id, project_group_id, container_path=None):
    """
    Remove user from group
    :param server_context:
    :param email:
    :param project_group:
    :param container_path:
    :return:
    """
    return __make_security_group_api_request(server_context, 'RemoveGroupMember.api', user_ids, project_group_id, container_path)


def __make_security_group_api_request(server_context, api, user_ids, group_id, container_path):
    """
    Execute a request against the LabKey Security Controller Group Membership apis
    :param server_context: Labkey Server context
    :param api: Action to execute
    :param user_ids: user ids to apply action to
    :param group_id: group id to apply action to
    :param container_path: Additional container context path
    :return: Request json object
    """
    url = build_url(server_context, security_controller, api, container_path)

    # if user_ids is only a single scalar make it an array
    if not hasattr(user_ids, "__iter__"):
        user_ids = [user_ids]

    payload = {
        'groupId': group_id,
        'principalIds': user_ids
    }

    return __make_request(server_context, url, payload)


def __make_security_role_api_request(server_context, api, role_name, email=None, user_id=None, container_path=None):
    """
    Execute a request against the LabKey Security Controller Group Membership apis
    :param server_context: Labkey Server context
    :param api: Action to execute
    :param user_id: user ids to apply action to
    :param role_name: group id to apply action to
    :param container_path: Additional container context path
    :return: Request json object
    """
    if email is None and user_id is None:
        raise ValueError("Must supply either/both [email] or [user_id]")

    url = build_url(server_context, security_controller, api, container_path)

    payload = {
        'roleClassName': role_name,
        'principalId': user_id,
        'email': email
    }

    return __make_request(server_context, url, payload)


def add_to_role(server_context, role, user_id=None, email=None, container_path=None):
    """
    Add user/group to security role
    :param server_context: LabKey server context
    :param role: to add user to
    :param user_id: to add permissions role to (must supply this or email or both)
    :param email: to add permissions role to (must supply this or user_id or both)
    :param container_path: additional project path context
    :return:
    """
    return __make_security_role_api_request(server_context, 'AddAssignment.api', role, user_id=user_id, email=email,
                                            container_path=container_path)


def remove_to_role(server_context, role, user_id=None, email=None, container_path=None):
    """
    Remove user/group from security role
    :param server_context: LabKey server context
    :param role: to remove user from
    :param user_id: to remove permissions from (must supply this or email or both)
    :param email: to remove permissions from (must supply this or user_id or both)
    :param container_path: additional project path context
    :return:
    """
    return __make_security_role_api_request(server_context, 'AddAssignment.api', role, user_id=user_id, email=email, container_path=container_path)


def rotate_password(server_context, user_id, password, container_path=None):
    """
    Change password for a user
    :param server_context:
    :param email:
    :param password:
    :param container_path:
    :return:
    """
    raise NotImplementedError("Not implemented yet")


def __make_request(server_context, url, payload=None, headers=None, timeout=_default_timeout):
    try:
        session = server_context['session']
        session.get(url)
        csrftoken = session.cookies['X-LABKEY-CSRF']
        print(url)
        if csrftoken is not None:
            if headers is None:
                headers = {}

            headers['X-LABKEY-CSRF'] = csrftoken

        raw_response = session.post(url, data=payload, headers=headers, timeout=timeout)
        return handle_response(raw_response)
    except SSLError as e:
        raise ServerContextError(e)
