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
from labkey.exceptions import ServerNotFoundError
from labkey.security import (
    create_user,
    delete_users,
    deactivate_users,
    add_to_group,
    add_to_role,
    reset_password,
    get_user_by_email,
    get_roles,
)
from labkey.utils import create_server_context

labkey_server = "localhost:8080"
project_name = "Home"  # Project folder name
contextPath = "labkey"
server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=False)


###############
# add User
###############
new_user_email = "demo@labkey.com"

result = create_user(server_context, new_user_email)
if result is not None:
    print(result)
else:
    print("Add users: no results returned")
    exit()


###############
# Show Users
###############
try:
    result = get_user_by_email(server_context, new_user_email)
except ValueError:
    print("User not found")

if result is not None:
    print(result)
else:
    print("Show users: no results returned")
    exit()


###############
# reset User's password
###############
new_user_id = result["userId"]
result = reset_password(server_context, new_user_email)
if result is not None:
    print(result)
else:
    print("Reset password: no results returned")
    exit()


###############
# add permissions to User
###############

# List Security Roles
result = get_roles(server_context)
if result is not None:
    print(result)
else:
    print("No results returned")
    exit()

author_role = None
for role in result["roles"]:
    if role["name"] == "Author":
        author_role = role

try:
    result = add_to_role(server_context, role=author_role, user_id=new_user_id)
except ServerNotFoundError:
    print("resource not found, check that '" + project_name + "' project exists")

if result is not None:
    print(result)
else:
    print("Add user permissions: no results returned")
    exit()


###############
# add user to group
###############
site_group_id = -1  # This needs to be the ID of a Project Group within the project specified above

if site_group_id == -1:
    print(
        "NOTE: To successfully complete this sample code a 'site_group_id' must be set in the file."
    )
    exit()

result = add_to_group(server_context, new_user_id, site_group_id)
if result is not None:
    print(result)
else:
    print("Add user to group: no results returned")
    exit()

###############
# deactivate User
###############

result = deactivate_users(server_context, [new_user_id])
if result is not None:
    print(result)
else:
    print("Deactivate user: no results returned")
    exit()


###############
# delete User
###############
result = delete_users(server_context, [new_user_id])
if result is not None:
    print(result)
else:
    print("Delete user: no results returned")
    exit()
