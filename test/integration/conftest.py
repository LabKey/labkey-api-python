import os
from configparser import ConfigParser

import pytest

from labkey.api_wrapper import APIWrapper
from labkey.server_context import ServerContext
from labkey import container
from labkey.exceptions import QueryNotFoundError

DEFAULT_HOST = "localhost"
DEFAULT_PORT = "8080"
DEFAULT_CONTEXT_PATH = "labkey"
PROJECT_NAME = "PythonIntegrationTests"


@pytest.fixture(scope="session")
def server_context_vars():
    properties_file_path = os.getenv("TEAMCITY_BUILD_PROPERTIES_FILE")
    host = os.getenv("HOST", DEFAULT_HOST)
    port = os.getenv("PORT", DEFAULT_PORT)
    context_path = os.getenv("CONTEXT_PATH", DEFAULT_CONTEXT_PATH)

    if properties_file_path is not None:
        with open(properties_file_path) as f:
            contents = f.read()
            # .properties files are ini files without any sections, so we need to inject one
            contents = "[config]\n" + contents
            parser = ConfigParser()
            parser.read_string(contents)
            parsed_config = parser["config"]
            host = parsed_config.get("labkey.server", DEFAULT_HOST)
            port = parsed_config.get("tomcat.port", DEFAULT_PORT)
            context_path = parsed_config.get("labkey.contextpath", DEFAULT_CONTEXT_PATH)

            if host.startswith("http://"):
                host = host.replace("http://", "")

            if context_path.startswith("/"):
                context_path = context_path[1:]

    return f"{host}:{port}", context_path


@pytest.fixture(scope="session")
def api(server_context_vars):
    server, context_path = server_context_vars
    api = APIWrapper(server, PROJECT_NAME, context_path, use_ssl=False)
    api.security.stop_impersonating()  # Call stop impersonating incase previous test run failed while impersonating a user.
    return api


@pytest.fixture(autouse=True, scope="session")
def project(server_context_vars):
    server, context_path = server_context_vars
    context = ServerContext(server, "", context_path, use_ssl=False)

    try:
        container.delete(context, PROJECT_NAME)
    except QueryNotFoundError:
        # The project may not exist, and that is ok.
        pass

    project_ = container.create(context, PROJECT_NAME, folder_type="Study")
    yield project_
    container.delete(context, PROJECT_NAME)
