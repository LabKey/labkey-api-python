#
# Copyright (c) 2022-2026 LabKey Corporation
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
from labkey.server_context import ServerContext, strip_slashes
import pytest

DEFAULT_CONTEXT = {"container_path": "test_container", "context_path": "test_context_path"}
BASE = "https://example.com/test_context_path"


@pytest.mark.parametrize(
    "context, expected",
    [
        pytest.param(DEFAULT_CONTEXT, BASE, id="default"),
        pytest.param(
            {**DEFAULT_CONTEXT, "use_ssl": False},
            "http://example.com/test_context_path",
            id="no-ssl",
        ),
        pytest.param(
            {"container_path": "test_container"}, "https://example.com", id="no-context-path"
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": "/test_context_path"},
            BASE,
            id="leading-slash",
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": "test_context_path/"},
            BASE,
            id="trailing-slash",
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": "/test_context_path/"},
            BASE,
            id="both-slashes",
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": "/"},
            "https://example.com",
            id="root",
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": ""},
            "https://example.com",
            id="empty",
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": "//test_context_path//"},
            BASE,
            id="repeated-slashes",
        ),
        pytest.param(
            {"container_path": "test_container", "context_path": "///"},
            "https://example.com",
            id="only-slashes",
        ),
    ],
)
def test_base_url(context, expected):
    assert ServerContext("example.com", **context).base_url == expected


@pytest.mark.parametrize(
    "context, container_path, expected",
    [
        pytest.param(DEFAULT_CONTEXT, None, f"{BASE}/test_container", id="default"),
        pytest.param(DEFAULT_CONTEXT, "other", f"{BASE}/other", id="override"),
        pytest.param(DEFAULT_CONTEXT, "/lead", f"{BASE}/lead", id="override-leading-slash"),
        pytest.param(DEFAULT_CONTEXT, "trail/", f"{BASE}/trail", id="override-trailing-slash"),
        pytest.param(DEFAULT_CONTEXT, "/both/", f"{BASE}/both", id="override-both-slashes"),
        pytest.param(
            DEFAULT_CONTEXT, "/parent/child/", f"{BASE}/parent/child", id="override-nested"
        ),
        pytest.param(DEFAULT_CONTEXT, "/", BASE, id="override-root"),
        pytest.param(DEFAULT_CONTEXT, "", BASE, id="override-empty"),
        pytest.param(
            {"container_path": "/test_container", "context_path": "/test_context_path"},
            None,
            f"{BASE}/test_container",
            id="context-leading-slashes",
        ),
        pytest.param(
            {"container_path": "test_container/", "context_path": "test_context_path/"},
            None,
            f"{BASE}/test_container",
            id="context-trailing-slashes",
        ),
        pytest.param(
            {"container_path": None, "context_path": "/test_context_path/"},
            None,
            BASE,
            id="no-container",
        ),
        pytest.param(
            {"container_path": "test_container"},
            None,
            "https://example.com/test_container",
            id="no-context-path",
        ),
        pytest.param(
            {"container_path": "test_container"},
            "/other/",
            "https://example.com/other",
            id="no-context-path-override",
        ),
        pytest.param(
            {"container_path": "/", "context_path": "/"}, None, "https://example.com", id="root"
        ),
        pytest.param(
            {"container_path": "/", "context_path": "/"},
            "/",
            "https://example.com",
            id="root-override-root",
        ),
        pytest.param(
            {"container_path": "", "context_path": ""}, None, "https://example.com", id="empty"
        ),
        pytest.param(DEFAULT_CONTEXT, "//other//", f"{BASE}/other", id="override-repeated-slashes"),
        pytest.param(DEFAULT_CONTEXT, "///", BASE, id="override-only-slashes"),
        pytest.param(
            {"container_path": "//test_container//", "context_path": "//test_context_path//"},
            None,
            f"{BASE}/test_container",
            id="context-repeated-slashes",
        ),
        pytest.param(
            {"container_path": "///", "context_path": "///"},
            None,
            "https://example.com",
            id="only-slashes",
        ),
    ],
)
def test_build_url(context, container_path, expected):
    server_context = ServerContext("example.com", **context)
    assert (
        server_context.build_url("query", "getQuery.api", container_path)
        == f"{expected}/query-getQuery.api"
    )


@pytest.mark.parametrize(
    "context, container_path, file_name, expected",
    [
        pytest.param(DEFAULT_CONTEXT, None, None, "/_webdav/test_container/@files", id="default"),
        pytest.param(
            DEFAULT_CONTEXT, None, "test.jpg", "/_webdav/test_container/@files/test.jpg", id="file"
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "/test.jpg",
            "/_webdav/test_container/@files/test.jpg",
            id="file-leading-slash",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "sub/test.jpg",
            "/_webdav/test_container/@files/sub/test.jpg",
            id="file-in-subfolder",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "some_folder/",
            "/_webdav/test_container/@files/some_folder/",
            id="folder",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "/some_folder/",
            "/_webdav/test_container/@files/some_folder/",
            id="folder-leading-slash",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "/parent/child/",
            "/_webdav/test_container/@files/parent/child/",
            id="folder-nested",
        ),
        pytest.param(DEFAULT_CONTEXT, None, "", "/_webdav/test_container/@files/", id="file-empty"),
        pytest.param(DEFAULT_CONTEXT, None, "/", "/_webdav/test_container/@files/", id="file-root"),
        pytest.param(
            DEFAULT_CONTEXT,
            "my_container/with_subfolder",
            "data.txt",
            "/_webdav/my_container/with_subfolder/@files/data.txt",
            id="override-nested",
        ),
        pytest.param(
            DEFAULT_CONTEXT, "/lead", None, "/_webdav/lead/@files", id="override-leading-slash"
        ),
        pytest.param(
            DEFAULT_CONTEXT, "trail/", None, "/_webdav/trail/@files", id="override-trailing-slash"
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            "/parent/child/",
            "data.txt",
            "/_webdav/parent/child/@files/data.txt",
            id="override-both-slashes",
        ),
        pytest.param(DEFAULT_CONTEXT, "/", None, "/_webdav/@files", id="override-root"),
        pytest.param(
            DEFAULT_CONTEXT, "/", "test.jpg", "/_webdav/@files/test.jpg", id="override-root-file"
        ),
        pytest.param(DEFAULT_CONTEXT, "", None, "/_webdav/@files", id="override-empty"),
        pytest.param(
            DEFAULT_CONTEXT, "", "test.jpg", "/_webdav/@files/test.jpg", id="override-empty-file"
        ),
        # Context path and scheme are not part of the webdav path
        pytest.param(
            {"container_path": "test_container"},
            None,
            None,
            "/_webdav/test_container/@files",
            id="no-context-path",
        ),
        pytest.param(
            {**DEFAULT_CONTEXT, "use_ssl": False},
            None,
            None,
            "/_webdav/test_container/@files",
            id="no-ssl",
        ),
        pytest.param(
            {"container_path": "/test_container/", "context_path": "test_context_path"},
            None,
            None,
            "/_webdav/test_container/@files",
            id="context-both-slashes",
        ),
        pytest.param(
            {"container_path": None, "context_path": "test_context_path"},
            None,
            None,
            "/_webdav/@files",
            id="no-container",
        ),
        pytest.param(
            {"container_path": None, "context_path": "test_context_path"},
            None,
            "test.jpg",
            "/_webdav/@files/test.jpg",
            id="no-container-file",
        ),
        pytest.param(
            {"container_path": "/", "context_path": "test_context_path"},
            None,
            None,
            "/_webdav/@files",
            id="root",
        ),
        pytest.param(
            {"container_path": "/", "context_path": "test_context_path"},
            None,
            "test.jpg",
            "/_webdav/@files/test.jpg",
            id="root-file",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "//test.jpg",
            "/_webdav/test_container/@files/test.jpg",
            id="file-repeated-leading-slashes",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            None,
            "//some_folder//",
            "/_webdav/test_container/@files/some_folder//",
            id="folder-repeated-slashes",
        ),
        pytest.param(
            DEFAULT_CONTEXT,
            "//parent/child//",
            "data.txt",
            "/_webdav/parent/child/@files/data.txt",
            id="override-repeated-slashes",
        ),
        pytest.param(DEFAULT_CONTEXT, "///", None, "/_webdav/@files", id="override-only-slashes"),
        pytest.param(
            {"container_path": "//test_container//", "context_path": "test_context_path"},
            None,
            None,
            "/_webdav/test_container/@files",
            id="context-repeated-slashes",
        ),
    ],
)
def test_webdav_path(context, container_path, file_name, expected):
    server_context = ServerContext("example.com", **context)
    assert server_context.webdav_path(container_path, file_name) == expected


def test_strip_slashes():
    assert strip_slashes(None) is None
    assert strip_slashes("/") is None
    assert strip_slashes("") is None
    assert strip_slashes("//") is None
    assert strip_slashes("///") is None
    assert strip_slashes("stuff") == "stuff"
    assert strip_slashes("/stuff") == "stuff"
    assert strip_slashes("stuff/") == "stuff"
    assert strip_slashes("/stuff/") == "stuff"
    assert strip_slashes("/parent/child/") == "parent/child"
    assert strip_slashes("//stuff//") == "stuff"
    assert strip_slashes("//parent//child//") == "parent//child"
