from labkey.utils import json_dumps, ServerContext


def create(
    server_context,
    name,
    container_path=None,
    description=None,
    folder_type=None,
    is_workbook=None,
    title=None,
):
    # type: (ServerContext, str, str, str, str, bool, str) -> dict
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
    headers = {"Content-Type": "application/json"}
    url = server_context.build_url("core", "createContainer.api", container_path)
    payload = {
        "description": description,
        "folderType": folder_type,
        "isWorkbook": is_workbook,
        "name": name,
        "title": title,
    }
    return server_context.make_request(url, json_dumps(payload), headers=headers)


def delete(server_context, container_path=None):
    # type: (ServerContext, str) -> any
    """
    Deletes a container at the given container_path, or at the server_context's container path
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param container_path: The path of the container to delete.
    :return:
    """
    headers = {"Content-Type": "application/json"}
    url = server_context.build_url("core", "deleteContainer.api", container_path)
    return server_context.make_request(url, None, headers=headers)
