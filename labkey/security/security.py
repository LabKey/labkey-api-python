

from __future__ import unicode_literals

from requests.exceptions import SSLError
from labkey.utils import build_url, handle_response
from labkey.exceptions import ServerContextError

_default_timeout = 60 * 5  # 5 minutes
security_controller = 'security'
user_controller = 'user'


def create_user(server_context, email, container_path=None, send_email=False, **kwargs):
    """
    Create new account (specify username, email and all other fields in user properties)
    :param server_context:
    :param email:
    :param container_path:
    :param send_email: true to send email notification to user
    :return:
    """
    url = build_url(server_context, security_controller, 'CreateNewUser.api', container_path)
    payload = {
        'email': email,
        'sendEmail': send_email
    }

    return __make_request(server_context, url, payload, **kwargs)


def activate_user(server_context, target_id, container_path=None, **kwargs):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_id:
    :param container_path:
    :return:
    """
    return activate_users(server_context, target_ids=[target_id], container_path=container_path, **kwargs)


def activate_users(server_context, target_ids, container_path=None, **kwargs):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_ids:
    :param container_path:
    :return:
    """
    return __make_user_api_request(server_context, target_ids=target_ids, api='ActivateUsers.api', container_path=container_path, **kwargs)


def deactivate_user(server_context, target_id, container_path=None, **kwargs):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_id:
    :param container_path:
    :return:
    """
    return deactivate_users(server_context, target_ids=[target_id], container_path=container_path, **kwargs)


def deactivate_users(server_context, target_ids, container_path=None, **kwargs):
    """
    Deactive but do not delete user account
    :param server_context:
    :param target_ids:
    :param container_path:
    :return:
    """
    result = __make_user_api_request(server_context, target_ids=target_ids, api='DeactivateUsers.api', container_path=container_path, **kwargs)
    if result is not None and result['status_code'] == 200:
        return dict(success=True)
    else:
        raise ValueError("Unable to delete users {0}".format(target_ids))


def delete_user(server_context, target_id, container_path=None, **kwargs):
    """
    Delete user account
    :param target_id:
    :param server_context:
    :param container_path:
    :return:
    """
    return delete_users(server_context, target_ids=[target_id], container_path=container_path, **kwargs)


def delete_users(server_context, target_ids, container_path=None, **kwargs):
    """
    Delete user account
    :param target_ids:
    :param server_context:
    :param container_path:
    :return:
    """
    result = __make_user_api_request(server_context, target_ids=target_ids, api='DeleteUsers.api', container_path=container_path, **kwargs)
    if result is not None and result['status_code'] == 200:
        return dict(success=True)
    else:
        raise ValueError("Unable to delete users {0}".format(target_ids))

def __make_user_api_request(server_context, target_ids, api, container_path=None, **kwargs):
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

    return __make_request(server_context, url, payload, **kwargs)


def add_to_group(server_context, user_ids, group_id, container_path=None, **kwargs):
    """
    Add user to group
    :param server_context: LabKey server context
    :param user_ids: users to add
    :param group_id: to add to
    :param container_path:
    :return:
    """
    return __make_security_group_api_request(server_context, 'AddGroupMember.api', user_ids, group_id, container_path, **kwargs)


def remove_from_group(server_context, user_ids, group_id, container_path=None, **kwargs):
    """
    Remove user from group
    :param server_context:
    :param user_ids:
    :param group_id:
    :param container_path:
    :return:
    """
    return __make_security_group_api_request(server_context, 'RemoveGroupMember.api', user_ids, group_id, container_path, **kwargs)


def __make_security_group_api_request(server_context, api, user_ids, group_id, container_path, **kwargs):
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

    return __make_request(server_context, url, payload, **kwargs)


def __make_security_role_api_request(server_context, api, role_name, email=None, user_id=None, container_path=None, **kwargs):
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

    return __make_request(server_context, url, payload, **kwargs)


def add_to_role(server_context, role, user_id=None, email=None, container_path=None, **kwargs):
    """
    Add user/group to security role
    :param server_context: LabKey server context
    :param role: to add user to
    :param user_id: to add permissions role to (must supply this or email or both)
    :param email: to add permissions role to (must supply this or user_id or both)
    :param container_path: additional project path context
    :return:
    """
    return __make_security_role_api_request(server_context, 'AddAssignment.api', role.get_unique_name(), user_id=user_id, email=email,
                                            container_path=container_path, **kwargs)


def remove_from_role(server_context, role, user_id=None, email=None, container_path=None, **kwargs):
    """
    Remove user/group from security role
    :param server_context: LabKey server context
    :param role: to remove user from
    :param user_id: to remove permissions from (must supply this or email or both)
    :param email: to remove permissions from (must supply this or user_id or both)
    :param container_path: additional project path context
    :return:
    """
    return __make_security_role_api_request(server_context, 'RemoveAssignment.api', role.get_unique_name(), user_id=user_id, email=email, container_path=container_path, **kwargs)


def reset_password(server_context, email, container_path=None, **kwargs):
    """
    Change password for a user  (Requires Admin privileges on the LabKey server)
    :param server_context:
    :param email:
    :param container_path:
    :return:
    """
    url = build_url(server_context, security_controller, 'adminRotatePassword.api', container_path)

    payload = {
        'email': email
    }

    return __make_request(server_context, url, payload, **kwargs)


def list_groups(server_context, include_site_groups=False, container_path=None, **kwargs):
    url = build_url(server_context, security_controller, 'listProjectGroups.api', container_path)

    payload = {
        'includeSiteGroups': include_site_groups
    }

    return __make_request(server_context, url, payload, **kwargs)


def get_user_by_email(server_context, email, **kwargs):

    url = build_url(server_context, user_controller, 'getUsers.api')
    payload = dict(includeDeactivatedAccounts=True)
    result = __make_request(server_context, url, payload, **kwargs)

    if result is None or result['users'] is None:
        raise ValueError("No Users in container" + email)

    for user in result['users']:
        if user['email'] == email:
            return user
    else:
        raise ValueError("User not found: " + email)


def __make_request(server_context, url, payload=None, headers=None, timeout=_default_timeout, **kwargs):
    try:
        session = server_context['session']
        raw_response = session.post(url, data=payload, headers=headers, timeout=timeout, **kwargs)
        return handle_response(raw_response)
    except SSLError as e:
        raise ServerContextError(e)
