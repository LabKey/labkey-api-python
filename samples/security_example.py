from __future__ import unicode_literals
from labkey.utils import create_server_context
from labkey.security.security import create_user, delete_user, deactivate_user, add_to_group, add_to_role\
    , reset_password, get_user_by_email
from labkey.security.roles import AuthorRole

print("Create a server context")
labkey_server = 'localhost:8080'
# project_name = 'Home'  # Project folder name
project_name = None
contextPath = 'labkey'
server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=False)

###############
# Test Show Users
###############
result = get_user_by_email(server_context, 'demo@labkey.com')
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test add User
###############
new_user_email = 'demoRocks@labkey.com'

result = create_user(server_context, new_user_email)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test reset User's password
###############
result = reset_password(server_context, new_user_email)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()

#
###############
# Test add permissions to User
###############
new_user_id = result['userId']

result = add_to_role(server_context, role=AuthorRole().get_unique_name(), user_id=new_user_id,
                     container_path='permissions test')
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test add user to group
###############
site_group_id = 1028

result = add_to_group(server_context, new_user_id, site_group_id)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()

project_group_id = 1029
result = add_to_group(server_context, new_user_id, project_group_id, container_path='permissions test')
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test deactivate User
###############
new_user_id = result['userId']

result = deactivate_user(server_context, new_user_id)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test delete User
###############
result = delete_user(server_context, new_user_id)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


