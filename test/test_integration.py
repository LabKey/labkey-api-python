import pytest

from labkey.exceptions import ServerContextError
from labkey.utils import create_server_context
from labkey.query import select_rows
from labkey import domain

SCHEMA_NAME = 'study'
QUERY_NAME = 'KrankenLevel'
DATASET_DOMAIN = {
    'kind': 'StudyDatasetVisit',
    'domainDesign': {
        'name': QUERY_NAME,
        'fields': [{
            'name': 'kronk',
            'label': 'krongggk',
            'rangeURI': 'double'
        }, {
            'name': 'type',
            'label': 'type',
            'rangeURI': 'string'
        }]
    }
}


@pytest.fixture
def server_context():
    """
    Use this fixture by adding an argument called "server_context" to your test function. It assumes you have a server
    running at localhost:8080, a project name "PythonIntegrationTest", and a context path of "labkey". You will need
    a netrc file configured with a valid username and password in order for API requests to work.

    :return: ServerContext
    """
    return create_server_context('localhost:8080', 'PythonIntegrationTest', 'labkey', use_ssl=False)


@pytest.fixture(scope="function")
def dataset(server_context):
    domain.create(server_context, DATASET_DOMAIN)
    created_domain = domain.get(server_context, SCHEMA_NAME, QUERY_NAME)
    yield created_domain
    # Clean up
    domain.drop(server_context, SCHEMA_NAME, QUERY_NAME)


@pytest.mark.integration
def test_select_rows(server_context):
    resp = select_rows(server_context, 'core', 'Users')
    assert resp['schemaName'] == 'core'
    assert resp['queryName'] == 'Users'
    assert resp['rowCount'] > 0
    assert len(resp['rows']) > 0


@pytest.mark.integration
def test_create_dataset(dataset):
    assert (dataset.name == QUERY_NAME)


@pytest.mark.integration
def test_create_duplicate_dataset(server_context, dataset):
    # Dataset fixture is not used directly here, but it is an argument so it gets created and cleaned up when this test
    # runs

    with pytest.raises(ServerContextError) as e:
        domain.create(server_context, DATASET_DOMAIN)

    assert e.value.message == f'\'500: A Dataset or Query already exists with the name "{QUERY_NAME}".\''
