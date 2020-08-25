import pytest

from labkey.utils import create_server_context
from labkey.query import select_rows


@pytest.fixture
def server_context():
    """
    Use this fixture by adding an argument called "server_context" to your test function. It assumes you have a server
    running at localhost:8080, a project name "PythonIntegrationTest", and a context path of "labkey". You will need
    a netrc file configured with a valid username and password in order for API requests to work.

    :return: ServerContext
    """
    return create_server_context('localhost:8080', 'PythonIntegrationTest', 'labkey', use_ssl=False)


@pytest.mark.integration
def test_select_rows(server_context):
    resp = select_rows(server_context, 'core', 'Users')
    assert resp['schemaName'] == 'core'
    assert resp['queryName'] == 'Users'
    assert resp['rowCount'] > 0
    assert len(resp['rows']) > 0
