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


def get_containers(
    server_context: ServerContext,
    container_path: str = None,
    include_effective_permissions: bool = True,
    include_subfolders: bool = False,
    depth: int = 50,
    include_standard_properties: bool = True,
):
    """
    Gets the containers for a given container_path
    :param server_context: a ServerContext object
    :param container_path: The container path to query against, defaults to the container path of the ServerContext
    :param include_effective_permissions: If set to false, the effective permissions for this container resource will
    not be included (defaults to True)
    :param include_subfolders: If set to true, the entire branch of containers will be returned. If false, only the
    immediate children of the starting container will be returned (defaults to False).
    :param depth: May be used to control the depth of recursion if includeSubfolders is set to true
    :param include_standard_properties: Includes the standard properties for containers, if f False returns a limited
    subset of properties: ['path', 'children', 'name', 'id'] (defaults to True)
    :return:
    """
    url = server_context.build_url("project", "getContainers.view", container_path=container_path)
    payload = {
        "includeSubfolders": include_subfolders,
        "includeEffectivePermissions": include_effective_permissions,
        "includeStandardProperties": include_standard_properties,
    }

    if include_subfolders:
        payload["depth"] = depth

    return server_context.make_request(url, json=payload)


class ContainerWrapper:
    """
    Wrapper for all the API methods exposed in the container module. Used by the APIWrapper class.
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
        self,
        name: str = None,
        title: str = None,
        add_alias: bool = True,
        container_path: str = None,
    ):
        return rename(self.server_context, name, title, add_alias, container_path)

    def get_containers(
        self,
        container_path: str = None,
        include_effective_permissions: bool = True,
        include_subfolders: bool = True,
        depth: int = 50,
        include_standard_properties: bool = True,
    ):
        return get_containers(
            self.server_context,
            container_path,
            include_effective_permissions,
            include_subfolders,
            depth,
            include_standard_properties,
        )
