from .server_context import ServerContext


def create(
    server_context: ServerContext,
    name: str,
    container_path: str = None,
    description: str = None,
    folder_type: str = None,
    is_workbook: bool = None,
    title: str = None,
) -> dict:
    """
    Create a container in LabKey.

    :param server_context: A LabKey server context. See utils.create_server_context.
    :param name: The name of the container.
    :param container_path: the path of where you want to create the container.
    :param description: a description for the container.
    :param folder_type: the desired folder type for the container.
    :param is_workbook: sets whether the container is a workbook.
    :param title: the title for the container.
    :return:
    """
    url = server_context.build_url("core", "createContainer.api", container_path)
    payload = {
        "description": description,
        "folderType": folder_type,
        "isWorkbook": is_workbook,
        "name": name,
        "title": title,
    }
    return server_context.make_request(url, json=payload)


def delete(server_context: ServerContext, container_path: str = None) -> any:
    """
    Deletes a container at the given container_path, or at the server_context's container path
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param container_path: The path of the container to delete.
    :return:
    """
    headers = {"Content-Type": "application/json"}
    url = server_context.build_url("core", "deleteContainer.api", container_path)
    return server_context.make_request(url, headers=headers)


def rename(
    server_context: ServerContext,
    name: str = None,
    title: str = None,
    add_alias: bool = True,
    container_path: str = None,
) -> any:
    """
    Renames a container at the given container_path, or at the server_context's container path
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param name: The new name of the container.
    :param title: The new title of the container.
    :param add_alias: Whether to add a folder alias for the folder's current name.
    :param container_path: The path of the container to rename.
    :return:
    """
    url = server_context.build_url("admin", "renameContainer.api", container_path)
    payload = {
        "name": name,
        "title": title,
        "addAlias": add_alias,
    }
    return server_context.make_request(url, json=payload)

def get_folders(
        server_context: ServerContext, 
        container_path: str = None,
        include_effective_permissions: bool = True, 
        include_subfolders: bool = False, 
        depth: int = 50,
        include_child_workbooks: bool = True, 
        include_standard_properties: bool = True
    ):
    
    # request parameters
    inclsf = "1" if include_subfolders else "0"
    inclep = "1" if include_effective_permissions else "0"
    inclcw = "1" if include_child_workbooks else "0"
    inclsp = "1" if include_standard_properties else "0"
    result_cols = ["name", "path", "id", "title", "type", "folderType", "effectivePermissions"] if include_standard_properties else ["name", "path", "id", "effectivePermissions"]

    #build url for request
    url = server_context.build_url('project', 'getContainers.view', container_path=container_path)
    payload = {
        'includeSubfolders': inclsf, 
        'includeEffectivePermissions': inclep, 
        'includeChildWorkbooks': inclcw,
        'includeStandardProperties': inclsp
    }
    
    if include_subfolders:
        payload['depth'] = depth
        
    #set list column headers
    if include_standard_properties:
        result_cols = ['name', 'path', 'id', 'title', 'type', 'folderType', 'effectivePermissions']
    else:
        result_cols = ['name', 'path', 'id', 'effectivePermissions']
    
    #make request and create output object
    data = server_context.make_request(url, json=payload)
    output = []
    output += [result_cols]

    # parse for current project
    row_starter = []
    for col in result_cols:
        if col != 'effectivePermissions':
            if data[col] is None:
                row_starter += ['']
            else:
                row_starter += [data[col]]
        elif col == 'effectivePermissions':
            for perm in data[col]:
                row = []
                row += row_starter
                row += [perm]
                output += [row]
    
    #parse for all children to current project
    for child in data['children']:
        row_starter = []
        for col in result_cols:
            if col != 'effectivePermissions':
                if child[col] is None:
                    row_starter += ['']
                else:
                    row_starter += [child[col]]
            elif col == 'effectivePermissions':
                for perm in child[col]:
                    row = []
                    row += row_starter
                    row += [perm]
                    output += [row]
    
    return output

class ContainerWrapper:
    """
    Wrapper for all of the API methods exposed in the container module. Used by the APIWrapper class.
    """

    def __init__(self, server_context: ServerContext):
        self.server_context = server_context

    def create(
        self,
        name: str,
        container_path: str = None,
        description: str = None,
        folder_type: str = None,
        is_workbook: bool = None,
        title: str = None,
    ):
        return create(
            self.server_context, name, container_path, description, folder_type, is_workbook, title
        )

    def delete(self, container_path: str = None):
        return delete(self.server_context, container_path)

    def rename(
        self, name: str = None, title: str = None, add_alias: bool = True, container_path: str = None
    ):
        return rename(self.server_context, name, title, add_alias, container_path)
        
    def get_folders(
        self,
        container_path: str = None,
        include_effective_permissions: bool = True, 
        include_subfolders: bool = True, 
        depth: int = 50,
        include_child_workbooks: bool = True, 
        include_standard_properties: bool = True
    ):
        return get_folders(
            self.server_context,
            container_path,
            include_effective_permissions, 
            include_subfolders, 
            depth,
            include_child_workbooks, 
            include_standard_properties
        )
