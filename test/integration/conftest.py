#
# Copyright (c) 2020-2026 LabKey Corporation
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
import os
import re
from configparser import ConfigParser

import pytest

from labkey.api_wrapper import APIWrapper
from labkey.server_context import ServerContext
from labkey import container
from labkey.exceptions import QueryNotFoundError

DEFAULT_PROTOCOL = "http"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "8080"
DEFAULT_CONTEXT_PATH = ""
PROJECT_NAME = "PythonIntegrationTests"


# TeamCity writes Java .properties, which escape ':' and '=' with a backslash; ConfigParser keeps the backslash.
# Blank parameters are treated as unset.
def get_property(config, name, default):
    value = config.get(name)
    if not value:
        return default
    return re.sub(r"\\(.)", r"\1", value)


def validate_server(protocol, host, port):
    url = f"{protocol}://{host}:{port}"
    error = f'Invalid integration server URL "{url}" built from protocol "{protocol}", host "{host}", port "{port}"'

    if protocol.lower() not in ("http", "https"):
        raise ValueError(f"{error}: protocol must be http or https")

    # A hostname, IPv4 address, or bracketed IPv6 address
    if not re.fullmatch(r"[A-Za-z0-9.-]+|\[[0-9A-Fa-f:.]+\]", host):
        raise ValueError(f"{error}: host must be a hostname or IP address without a protocol, port, or path")

    if not port.isdigit() or not 0 < int(port) < 65536:
        raise ValueError(f"{error}: port must be a number between 1 and 65535")


@pytest.fixture(scope="session")
def server_context_vars():
    properties_file_path = os.getenv("TEAMCITY_BUILD_PROPERTIES_FILE")
    protocol = os.getenv("PROTOCOL", DEFAULT_PROTOCOL)
    host = os.getenv("HOST", DEFAULT_HOST)
    port = os.getenv("PORT", DEFAULT_PORT)
    context_path = os.getenv("CONTEXT_PATH", DEFAULT_CONTEXT_PATH)
    # Off by default so tests can run against servers with self-signed certificates
    verify_ssl = os.getenv("VERIFY_SSL", "false").lower() in ("true", "1", "yes")

    if properties_file_path is not None:
        with open(properties_file_path) as f:
            contents = f.read()
            # .properties files are ini files without any sections, so we need to inject one
            contents = "[config]\n" + contents
            parser = ConfigParser()
            parser.read_string(contents)
            parsed_config = parser["config"]
            # Missing or blank parameters fall back to the environment variables or defaults
            host = get_property(parsed_config, "labkey.server", host)
            # labkey.port takes precedence over tomcat.port, which is set on TeamCity build agents
            port = get_property(parsed_config, "labkey.port", get_property(parsed_config, "tomcat.port", port))
            context_path = get_property(parsed_config, "labkey.contextpath", context_path)

            if "://" in host:
                protocol, host = host.split("://", 1)

            if context_path.startswith("/"):
                context_path = context_path[1:]

    validate_server(protocol, host, port)
    use_ssl = protocol.lower() == "https"
    return f"{host}:{port}", context_path, use_ssl, verify_ssl


@pytest.fixture(scope="session")
def api(server_context_vars):
    server, context_path, use_ssl, verify_ssl = server_context_vars
    api = APIWrapper(server, PROJECT_NAME, context_path, use_ssl=use_ssl, verify_ssl=verify_ssl)
    api.security.stop_impersonating()  # Call stop impersonating incase previous test run failed while impersonating a user.
    return api


@pytest.fixture(autouse=True, scope="session")
def project(server_context_vars):
    server, context_path, use_ssl, verify_ssl = server_context_vars
    context = ServerContext(server, "", context_path, use_ssl=use_ssl, verify_ssl=verify_ssl)

    try:
        container.delete(context, PROJECT_NAME)
    except QueryNotFoundError:
        # The project may not exist, and that is ok.
        pass

    project_ = container.create(context, PROJECT_NAME, folder_type="Study")
    yield project_
    container.delete(context, PROJECT_NAME)
