import os
from configparser import ConfigParser

import pytest

from labkey.domain import conditional_format
from labkey.exceptions import ServerContextError
from labkey.utils import create_server_context
from labkey.query import delete_rows, insert_rows, select_rows, update_rows
from labkey import domain, container

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '8080'
DEFAULT_CONTEXT_PATH = 'labkey'
PROJECT_NAME = 'PythonIntegrationTests'
STUDY_NAME = 'TestStudy'
SCHEMA_NAME = 'study'
QUERY_NAME = 'KrankenLevel'
DATASET_DOMAIN = {
    'kind': 'StudyDatasetVisit',
    'domainDesign': {
        'name': QUERY_NAME,
        'fields': [
            {'name': 'kronk', 'label': 'krongggk', 'rangeURI': 'double'},
            {'name': 'type', 'label': 'type', 'rangeURI': 'string'},
        ],
    }
}
TEST_QC_STATES = [
    {'label': 'needs verification', 'description': 'that can not be right', 'publicData': False},
    {'label': 'approved', 'publicData': True},
]

LISTS_SCHEMA = 'lists'
LIST_NAME = 'testlist'
CONDITIONAL_FORMAT = [{
               'filter': 'format.column~gte=25',
               'textcolor': 'ff0000',
               'backgroundcolor': 'ffffff',
               'bold' : True,
               'italic' : False,
               'strikethrough' : False
           }]
LIST_DEFINITION ={
   'kind': 'IntList',
   'domainDesign': {
       'name': LIST_NAME,
       'fields': [{
           'name': 'rowId',
           'rangeURI': 'int'
       }, {
           'name': 'formatted',
           'rangeURI': 'int',
           'conditionalFormats': CONDITIONAL_FORMAT
       }]
   },
   'options': {
       'keyName': 'rowId',
       'keyType': 'AutoIncrementInteger'
   }
}


@pytest.fixture(scope='session')
def server_context_vars():
    properties_file_path = os.getenv('TEAMCITY_BUILD_PROPERTIES_FILE')
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    context_path = DEFAULT_CONTEXT_PATH

    if properties_file_path is not None:
        with open(properties_file_path) as f:
            contents = f.read()
            # .properties files are ini files without any sections, so we need to inject one
            contents = '[config]\n' + contents
            parser = ConfigParser()
            parser.read_string(contents)
            parsed_config = parser['config']
            host = parsed_config.get('labkey.server', DEFAULT_HOST)
            port = parsed_config.get('tomcat.port', DEFAULT_PORT)
            context_path = parsed_config.get('labkey.contextpath', DEFAULT_CONTEXT_PATH)

            if host.startswith('http://'):
                host = host.replace('http://', '')

            if context_path.startswith('/'):
                context_path = context_path[1:]

    return f'{host}:{port}', context_path


@pytest.fixture(autouse=True, scope="session")
def project(server_context_vars):
    server, context_path = server_context_vars
    context = create_server_context(server, '', context_path, use_ssl=False)
    container.delete(context, PROJECT_NAME)
    project_ = container.create(context, PROJECT_NAME, folderType='study')
    yield project_
    container.delete(context, PROJECT_NAME)


@pytest.fixture(scope="session")
def server_context(server_context_vars):
    """
    Use this fixture by adding an argument called "server_context" to your test function. It assumes you have a server
    running at localhost:8080, a project name "PythonIntegrationTest", and a context path of "labkey". You will need
    a netrc file configured with a valid username and password in order for API requests to work.

    :return: ServerContext
    """
    server, context_path = server_context_vars
    return create_server_context(server, PROJECT_NAME, context_path, use_ssl=False)


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
def qc_states(server_context, study):
    insert_result = insert_rows(server_context, 'core', 'qcstate', TEST_QC_STATES)
    yield insert_result
    # clean up
    cleanup_qc_states= [
        {'rowId': insert_result['rows'][0]['rowid']},
        {'rowId': insert_result['rows'][1]['rowid']},
    ]
    delete_rows(server_context, 'core', 'qcstate', cleanup_qc_states)


@pytest.fixture(scope="function")
def create_list(server_context, project):
    domain.create(server_context, LIST_DEFINITION)
    created_list = domain.get(server_context, LISTS_SCHEMA, LIST_NAME)
    yield created_list
    #clean up
    domain.drop(server_context, LISTS_SCHEMA, LIST_NAME)


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


def test_create_qc_state_definition(server_context, qc_states):
    assert qc_states['rowsAffected'] == 2
    assert qc_states['rows'][0]['label'] == 'needs verification'
    assert qc_states['rows'][1]['label'] == 'approved'


def test_update_qc_state_definition(server_context, qc_states, study):
    new_description = 'for sure that is not right'
    edit_rowid = qc_states['rows'][0]['rowid']
    assert qc_states['rows'][0]['description'] != new_description
    to_edit_row = [{'rowid': edit_rowid, 'description': new_description}]
    update_response = update_rows(server_context, 'core', 'qcstate', to_edit_row)
    assert update_response['rowsAffected'] == 1
    assert update_response['rows'][0]['description'] == new_description


def test_insert_duplicate_labeled_qc_state_produces_error(server_context, qc_states, study):
    with pytest.raises(ServerContextError) as e:
        dupe_qc_state = [{'label': 'needs verification', 'publicData': 'false'}]
        insert_rows(server_context, 'core', 'qcstate', dupe_qc_state)
    
    assert "500: ERROR: duplicate key value violates unique constraint" in e.value.message


def test_cannot_delete_qc_state_in_use(server_context, qc_states, study, dataset):
    qc_state_rowid = qc_states['rows'][0]['rowid']
    new_row = [{
        'ParticipantId': '2',
        'vitd': 4,
        'SequenceNum': '345',
        'QCState': qc_state_rowid
    }]
    insert_result = insert_rows(server_context, SCHEMA_NAME, QUERY_NAME, new_row)
    inserted_lsid = insert_result['rows'][0]['lsid']
    assert insert_result['rowsAffected'] == 1
    assert insert_result['rows'][0]['QCState'] == qc_state_rowid

    with pytest.raises(ServerContextError) as e:
        qc_state_to_delete = [{'rowid': qc_state_rowid}]
        delete_rows(server_context, 'core', 'qcstate', qc_state_to_delete)

    assert  e.value.message == '"400: QC state \'needs verification\' cannot be deleted as it is currently in use."'
    # now clean up/stop using it
    dataset_row_to_remove = [{'lsid': inserted_lsid}]
    delete_rows(server_context, SCHEMA_NAME, QUERY_NAME, dataset_row_to_remove)


def test_add_conditional_format(server_context, project, create_list):
    new_conditional_format = conditional_format(
               query_filter='format.column~lte=7',
               text_color='ff0055',
               background_color='ffffff',
               bold=True,
               italic=False,
               strike_through=False
           )
    for field in create_list.fields:
        if field.name == 'formatted':
            field.conditional_formats.append(new_conditional_format)
    domain.save(server_context, LISTS_SCHEMA, LIST_NAME, create_list)
    saved_domain = domain.get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats.__len__() == 2