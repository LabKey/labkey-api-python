import pytest

from labkey.exceptions import ServerContextError
from labkey.utils import create_server_context
from labkey.query import delete_rows, insert_rows, select_rows, update_rows
from labkey import domain, container

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
PROJECT_NAME = 'PythonIntegrationTests'
STUDY_NAME = 'TestStudy'
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
TEST_QCSTATES = [{
        'label': 'needs verification',
        'description': 'that can not be right',
        'publicData': False
    }, {
        'label': 'approved',
        'publicData': True
    }]


@pytest.fixture(autouse=True, scope="session")
def project():
    context = create_server_context('localhost:8080', '', 'labkey', use_ssl=False)
    project_ = container.create(context, PROJECT_NAME, folderType='study')
    yield project_
    container.delete(context, PROJECT_NAME)


@pytest.fixture(scope="session")
def server_context():
    """
    Use this fixture by adding an argument called "server_context" to your test function. It assumes you have a server
    running at localhost:8080, a project name "PythonIntegrationTest", and a context path of "labkey". You will need
    a netrc file configured with a valid username and password in order for API requests to work.

    :return: ServerContext
    """
    return create_server_context('localhost:8080', PROJECT_NAME, 'labkey', use_ssl=False)


@pytest.fixture(scope="session")
def study(server_context):
    url = server_context.build_url('study', 'createStudy.view')
    payload = {
        'shareVisits': 'false',
        'shareDatasets': 'false',
        'simpleRepository': 'true',
        'securityString': 'BASIC_READ',
        'defaultTimepointDuration': '1',
        'startDate': '2020-01-01',
        'timepointType': 'VISIT',
        'subjectColumnName': 'PeopleId',
        'subjectNounPlural': 'Peoples',
        'subjectNounSingular': 'People',
        'label': 'Python Integration Tests Study'
    }
    created_study = server_context.make_request(url, payload, non_json_response=True)
    yield created_study
    url = server_context.build_url('study', 'deleteStudy.view')
    server_context.make_request(url, {'confirm': 'true'}, non_json_response=True)


@pytest.fixture(scope="session")
def dataset(server_context, study):
    # study is not used in this function, but the fixture is required to run because we need a study in order to create
    # a dataset
    domain.create(server_context, DATASET_DOMAIN)
    created_domain = domain.get(server_context, SCHEMA_NAME, QUERY_NAME)
    yield created_domain
    # Clean up
    domain.drop(server_context, SCHEMA_NAME, QUERY_NAME)


@pytest.fixture(scope="function")
def qcstates(server_context, study):
    insert_result = insert_rows(server_context, 'core', 'qcstate', TEST_QCSTATES)
    yield insert_result
    # clean up
    cleanup_qcStates= [{
        'rowId': insert_result['rows'][0]['rowid']
    }, {
        'rowId': insert_result['rows'][1]['rowid']
    }]
    delete_rows(server_context, 'core', 'qcstate', cleanup_qcStates)


def test_select_rows(server_context):
    resp = select_rows(server_context, 'core', 'Users')
    assert resp['schemaName'] == 'core'
    assert resp['queryName'] == 'Users'
    assert resp['rowCount'] > 0
    assert len(resp['rows']) > 0


def test_create_dataset(dataset):
    assert (dataset.name == QUERY_NAME)


def test_create_duplicate_dataset(server_context, dataset):
    # Dataset fixture is not used directly here, but it is an argument so it gets created and cleaned up when this test
    # runs

    with pytest.raises(ServerContextError) as e:
        domain.create(server_context, DATASET_DOMAIN)

    assert e.value.message == f'\'500: A Dataset or Query already exists with the name "{QUERY_NAME}".\''


def test_create_qcstate_definition(server_context, qcstates):
    assert qcstates['rowsAffected'] == 2
    assert qcstates['rows'][0]['label'] == 'needs verification'
    assert qcstates['rows'][1]['label'] == 'approved'


def test_update_qcstate_definition(server_context, qcstates, study):
    new_description = 'for sure that is not right'
    edit_rowid = qcstates['rows'][0]['rowid']
    assert qcstates['rows'][0]['description'] != new_description
    to_edit_row = [{'rowid': edit_rowid,
                    'description': new_description}]
    update_response = update_rows(server_context, 'core', 'qcstate', to_edit_row)
    assert update_response['rowsAffected'] == 1
    assert update_response['rows'][0]['description'] == new_description


def test_insert_duplicate_labeled_qcstate_produces_error(server_context, qcstates, study):
    with pytest.raises(ServerContextError) as e:
        dupe_qcstate = [{
            'label': 'needs verification',
            'publicData': 'false'
        }]
        insert_rows(server_context, 'core', 'qcstate', dupe_qcstate)
    assert "500: ERROR: duplicate key value violates unique constraint" in e.value.message


def test_cannot_delete_qcstate_in_use(server_context, qcstates, study, dataset):
    qcstate_rowid = qcstates['rows'][0]['rowid']
    new_row = [{'ParticipantId': '2',
                'vitd': 4,
                'SequenceNum': '345',
                'QCState': qcstate_rowid}]
    insert_result = insert_rows(server_context, SCHEMA_NAME, QUERY_NAME, new_row)
    inserted_lsid = insert_result['rows'][0]['lsid']
    assert insert_result['rowsAffected'] == 1
    assert insert_result['rows'][0]['QCState'] == qcstate_rowid

    with pytest.raises(ServerContextError) as e:
        qcstate_to_delete = [{'rowid': qcstate_rowid}]
        delete_rows(server_context, 'core', 'qcstate', qcstate_to_delete)
    assert  e.value.message == '"400: QC state \'needs verification\' cannot be deleted as it is currently in use."'
    # now clean up/stop using it
    dataset_row_to_remove = [{'lsid': inserted_lsid}]
    delete_rows(server_context, SCHEMA_NAME, QUERY_NAME, dataset_row_to_remove)
