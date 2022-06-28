from labkey.server_context import ServerContext
import pytest


@pytest.fixture(scope="session")
def server_context():
    return ServerContext("example.com", "test_container", "test_context_path")


@pytest.fixture(scope="session")
def server_context_no_context_path():
    return ServerContext("example.com", "test_container")


@pytest.fixture(scope="session")
def server_context_no_ssl():
    return ServerContext("example.com", "test_container", "test_context_path", use_ssl=False)


def test_base_url(server_context, server_context_no_context_path, server_context_no_ssl):
    assert server_context.base_url == "https://example.com/test_context_path"
    assert server_context_no_context_path.base_url == "https://example.com"
    assert server_context_no_ssl.base_url == "http://example.com/test_context_path"


def test_build_url(server_context):
    assert (
        server_context.build_url("query", "getQuery.api")
        == "https://example.com/test_context_path/test_container/query-getQuery.api"
    )
    assert (
        server_context.build_url("query", "getQuery.api", "different_container")
        == "https://example.com/test_context_path/different_container/query-getQuery.api"
    )


def test_webdav_path(server_context, server_context_no_context_path, server_context_no_ssl):
    assert server_context.webdav_path() == "/_webdav/test_container/@files"
    assert (
        server_context.webdav_path(file_name="test.jpg")
        == "/_webdav/test_container/@files/test.jpg"
    )
    assert (
        server_context.webdav_path("my_container/with_subfolder", "data.txt")
        == "/_webdav/my_container/with_subfolder/@files/data.txt"
    )
