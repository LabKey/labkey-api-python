import pytest

from labkey.api_wrapper import APIWrapper
from labkey.exceptions import ServerContextError

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
STUDY_NAME = "TestStudy"
SCHEMA_NAME = "study"
QUERY_NAME = "KrankenLevel"
DATASET_DOMAIN = {
    "kind": "StudyDatasetVisit",
    "domainDesign": {
        "name": QUERY_NAME,
        "fields": [
            {"name": "kronk", "label": "krongggk", "rangeURI": "double"},
            {"name": "type", "label": "type", "rangeURI": "string"},
        ],
    },
}
TEST_QC_STATES = [
    {
        "label": "needs verification",
        "description": "that can not be right",
        "publicData": False,
    },
    {"label": "approved", "publicData": True},
]


@pytest.fixture(scope="session")
def study(api: APIWrapper):
    url = api.server_context.build_url("study", "createStudy.view")
    payload = {
        "shareVisits": "false",
        "shareDatasets": "false",
        "simpleRepository": "true",
        "securityString": "BASIC_READ",
        "defaultTimepointDuration": "1",
        "startDate": "2020-01-01",
        "timepointType": "VISIT",
        "subjectColumnName": "PeopleId",
        "subjectNounPlural": "Peoples",
        "subjectNounSingular": "People",
        "label": "Python Integration Tests Study",
    }
    created_study = api.server_context.make_request(url, payload, non_json_response=True)
    yield created_study
    url = api.server_context.build_url("study", "deleteStudy.view")
    api.server_context.make_request(url, {"confirm": "true"}, non_json_response=True)


@pytest.fixture(scope="session")
def dataset(api: APIWrapper, study):
    # study is not used in this function, but the fixture is required to run because we need a study in order to create
    # a dataset
    api.domain.create(DATASET_DOMAIN)
    created_domain = api.domain.get(SCHEMA_NAME, QUERY_NAME)
    yield created_domain
    # Clean up
    api.domain.drop(SCHEMA_NAME, QUERY_NAME)


@pytest.fixture(scope="function")
def qc_states(api: APIWrapper, study):
    insert_result = api.query.insert_rows("core", "qcstate", TEST_QC_STATES)
    yield insert_result
    # clean up
    cleanup_qc_states = [
        {"rowId": insert_result["rows"][0]["rowid"]},
        {"rowId": insert_result["rows"][1]["rowid"]},
    ]
    api.query.delete_rows("core", "qcstate", cleanup_qc_states)


def test_api_select_rows(api: APIWrapper):
    resp = api.query.select_rows("core", "Users")
    assert resp["schemaName"] == "core"
    assert resp["queryName"] == "Users"
    assert resp["rowCount"] > 0
    assert len(resp["rows"]) > 0


def test_create_dataset(dataset):
    assert dataset.name == QUERY_NAME


def test_create_duplicate_dataset(api: APIWrapper, dataset):
    # Dataset fixture is not used directly here, but it is an argument so it gets created and cleaned up when this test
    # runs
    with pytest.raises(ServerContextError) as e:
        api.domain.create(DATASET_DOMAIN)

    expected = f"'500: A Dataset or Query already exists with the name \"{QUERY_NAME}\".'"
    assert e.value.message == expected


def test_create_qc_state_definition(qc_states):
    assert qc_states["rowsAffected"] == 2
    assert qc_states["rows"][0]["label"] == "needs verification"
    assert qc_states["rows"][1]["label"] == "approved"


def test_update_qc_state_definition(api: APIWrapper, qc_states, study):
    new_description = "for sure that is not right"
    edit_rowid = qc_states["rows"][0]["rowid"]
    assert qc_states["rows"][0]["description"] != new_description
    to_edit_row = [{"rowid": edit_rowid, "description": new_description}]
    update_response = api.query.update_rows("core", "qcstate", to_edit_row)
    assert update_response["rowsAffected"] == 1
    assert update_response["rows"][0]["description"] == new_description


def test_insert_duplicate_labeled_qc_state_produces_error(api: APIWrapper, qc_states, study):
    with pytest.raises(ServerContextError) as e:
        dupe_qc_state = [{"label": "needs verification", "publicData": "false"}]
        api.query.insert_rows("core", "qcstate", dupe_qc_state)

    assert "500: ERROR: duplicate key value violates unique constraint" in e.value.message


def test_cannot_delete_qc_state_in_use(api: APIWrapper, qc_states, study, dataset):
    qc_state_rowid = qc_states["rows"][0]["rowid"]
    new_row = [
        {
            "ParticipantId": "2",
            "vitd": 4,
            "SequenceNum": "345",
            "QCState": qc_state_rowid,
        }
    ]
    insert_result = api.query.insert_rows(SCHEMA_NAME, QUERY_NAME, new_row)
    inserted_lsid = insert_result["rows"][0]["lsid"]
    assert insert_result["rowsAffected"] == 1
    assert insert_result["rows"][0]["QCState"] == qc_state_rowid

    with pytest.raises(ServerContextError) as e:
        qc_state_to_delete = [{"rowid": qc_state_rowid}]
        api.query.delete_rows("core", "qcstate", qc_state_to_delete)

    assert (
        e.value.message
        == "\"400: QC state 'needs verification' cannot be deleted as it is currently in use.\""
    )
    # now clean up/stop using it
    dataset_row_to_remove = [{"lsid": inserted_lsid}]
    api.query.delete_rows(SCHEMA_NAME, QUERY_NAME, dataset_row_to_remove)
