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
from labkey.api_wrapper import APIWrapper

labkey_server = "localhost:8080"
project_name = "Home"  # Project folder name
context_path = "labkey"
api = APIWrapper(labkey_server, project_name, context_path, use_ssl=False)


###############
# Create Container
###############
create_response = api.container.create("newContainer", folder_type="Collaboration")
if "title" in create_response:
    print(create_response["title"] + " has been created")


###############
# Rename Container
###############
rename_response = api.container.rename("newContainerA")
if "title" in rename_response:
    print(create_response["title"] + " has been renamed to " + rename_response["title"])


###############
# Delete Container
###############
delete_response = api.container.delete("Home/" + rename_response["title"])
print(rename_response["title"] + "deleted")
