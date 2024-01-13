# LabKey Container API Overview

Create, update, or delete a LabKey container as well as get a list of LabKey containers.

In LabKey Server, a "container" is a fundamental organizational and security concept. It is a versatile and powerful feature that serves as a primary means to organize and manage data, users, and permissions.

For more info about LabKey containers (also referred to as Projects, Folders, and Subfolders) see here, https://www.labkey.org/Documentation/wiki-page.view?name=projects.

### LabKey Container API Methods

To use the container API methods, you must first instantiate an APIWrapper object. See the APIWrapper docs page to learn more about how to properly do so, accounting for your LabKey Server's configuration details. See the section Examples for more information on how these container API methods are used.

**create**

List of method parameters:
- name: The name of the container.
- container_path: the path of where you want to create the container.
- description: a description for the container.
- folder_type: the desired folder type for the container. Please note that the casing of folder_type string characters must be correct. Otherwise a "Custom" folder type will be created.
- is_workbook: sets whether the container is a workbook.
- title: the title for the container.

**delete**

List of method parameters:
- container_path: The path of the container to delete.

**rename**

List of method parameters:
- name: The new name of the container.
- title: The new title of the container.
- add_alias: Whether to add a folder alias for the folder's current name. In most cases, this should be left True. If set to False, then any queries, pipeline jobs, or other hardcoded references to the old container name will no longer be recognized.
- container_path: The path of the container to rename.

**get_containers**

List of method parameters:
- container_path: The container path to query against, defaults to the container path of the ServerContext
- include_effective_permissions: If set to false, the effective permissions for this container resource will not be included (defaults to True)
- include_subfolders: If set to true, the entire branch of containers will be returned. If false, only the immediate children of the starting container will be returned (defaults to False).
- depth: May be used to control the depth of recursion if includeSubfolders is set to true
- include_standard_properties: Includes the standard properties for containers, if f False returns a limited
- subset of properties: ['path', 'children', 'name', 'id'] (defaults to True)

### Examples

```python
from labkey.api_wrapper import APIWrapper

print("Create an APIWrapper")
labkey_server = 'localhost:8080'
project_name = 'ModuleAssayTest'  # Project folder name
contextPath = 'labkey'
schema = 'core'
table = 'Users'
api = APIWrapper(labkey_server, project_name, contextPath, use_ssl=False)

#create example
create_response = api.container.create(name = 'created_folder',
                                       description = 'This folder was created with the LabKey Python API.',
                                       folder_type = 'Study',
                                       title = 'Created Folder')

#rename example
rename_response = api.container.rename(container_path='joe_sandbox/created_folder',
                                       name = 'renamed_folder',
                                       title = 'Renamed Folder')

#delete example
delete_response = api.container.delete(container_path='joe_sandbox/renamed_folder')

#get_containers example
get_containers_response = api.container.get_containers(include_effective_permissions=True,
                                                       include_subfolders=True,
                                                       depth=1,
                                                       include_standard_properties=True)
```
