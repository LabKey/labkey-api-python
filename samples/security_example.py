from __future__ import unicode_literals

from labkey.exceptions import ServerNotFoundError
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
# Test add User
###############
new_user_email = 'demo@labkey.com'

result = create_user(server_context, new_user_email)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test Show Users
###############
try:
    result = get_user_by_email(server_context, new_user_email)
except ValueError:
    print("User not found")

if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test reset User's password
###############
new_user_id = result['userId']
result = reset_password(server_context, new_user_email)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test add permissions to User
###############
try:
    result = add_to_role(server_context, role=AuthorRole(), user_id=new_user_id, container_path='home')
except ServerNotFoundError:
    print("resource not found, check that 'Home' project is created")

if result is not None:
    print(result)
else:
    print("No results returned")
    exit()


###############
# Test add user to group
###############
site_group_id = -1

result = add_to_group(server_context, new_user_id, site_group_id)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()

###############
# Test deactivate User
###############

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


