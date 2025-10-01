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
    created_study = api.server_context.make_request(
        url, payload, non_json_response=True, allow_redirects=True
    )
    yield created_study
    url = api.server_context.build_url("study", "deleteStudy.view")
    api.server_context.make_request(
        url, {"confirm": "true"}, non_json_response=True, allow_redirects=True
    )


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
    print(api.security.who_am_i())
    insert_result = api.query.insert_rows("core", "datastates", TEST_QC_STATES)
    yield insert_result
    # clean up
    cleanup_qc_states = [
        {"rowId": insert_result["rows"][0]["rowid"]},
        {"rowId": insert_result["rows"][1]["rowid"]},
    ]
    api.query.delete_rows("core", "datastates", cleanup_qc_states)


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

    expected = f'500: A Dataset or Query already exists with the name "{QUERY_NAME}".'
    assert e.value.message == expected


def test_create_qc_state_definition(qc_states):
    assert qc_states["rowsAffected"] == 2
    assert qc_states["rows"][0]["label"] == "needs verification"
    assert qc_states["rows"][1]["label"] == "approved"


def test_execute_sql(api: APIWrapper):
    resp = api.query.execute_sql("core", "SELECT userId FROM core.users LIMIT 1")
    assert resp["schemaName"] == "core"
    assert resp["queryName"] == "sql"
    assert resp["rowCount"] > 0
    assert len(resp["rows"]) > 0


def test_update_qc_state_definition(api: APIWrapper, qc_states, study):
    new_description = "for sure that is not right"
    edit_rowid = qc_states["rows"][0]["rowid"]
    assert qc_states["rows"][0]["description"] != new_description
    to_edit_row = [{"rowid": edit_rowid, "description": new_description}]
    update_response = api.query.update_rows("core", "datastates", to_edit_row)
    assert update_response["rowsAffected"] == 1
    assert update_response["rows"][0]["description"] == new_description


def test_insert_duplicate_labeled_qc_state_produces_error(api: APIWrapper, qc_states, study):
    with pytest.raises(ServerContextError) as e:
        dupe_qc_state = [{"label": "needs verification", "publicData": "false"}]
        api.query.insert_rows("core", "datastates", dupe_qc_state)

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
        api.query.delete_rows("core", "datastates", qc_state_to_delete)

    assert (
        e.value.message
        == "400: State 'needs verification' cannot be deleted as it is currently in use."
    )
    # now clean up/stop using it
    dataset_row_to_remove = [{"lsid": inserted_lsid}]
    api.query.delete_rows(SCHEMA_NAME, QUERY_NAME, dataset_row_to_remove)


LISTS_SCHEMA = "lists"
PARENT_LIST_NAME = "parent_list"
PARENT_LIST_DEFINITION = {
    "kind": "IntList",
    "domainDesign": {
        "name": PARENT_LIST_NAME,
        "fields": [
            {"name": "rowId", "rangeURI": "int"},
            {
                "name": "name",
                "rangeURI": "string",
                "required": True,
            },
        ],
    },
    "indices": {
        "columnNames": ["name"],
        "unique": True,
    },
    "options": {"keyName": "rowId", "keyType": "AutoIncrementInteger"},
}
CHILD_LIST_NAME = "child_list"
CHILD_LIST_DEFINITION = {
    "kind": "IntList",
    "domainDesign": {
        "name": CHILD_LIST_NAME,
        "fields": [
            {"name": "rowId", "rangeURI": "int"},
            {
                "name": "name",
                "rangeURI": "string",
                "required": True,
            },
            {
                "name": "parent",
                "lookupQuery": "parent_list",
                "lookupSchema": "lists",
                "rangeURI": "int",
            },
        ],
    },
    "options": {"keyName": "rowId", "keyType": "AutoIncrementInteger"},
}

parent_data = """name
parent_one
parent_two
parent_three
"""

child_data = """name,parent
child_one,parent_one
child_two,parent_two
child_three,parent_three
"""


@pytest.fixture
def parent_list_fixture(api: APIWrapper):
    api.domain.create(PARENT_LIST_DEFINITION)
    created_list = api.domain.get(LISTS_SCHEMA, PARENT_LIST_NAME)
    yield created_list
    # clean up
    api.domain.drop(LISTS_SCHEMA, PARENT_LIST_NAME)


@pytest.fixture
def child_list_fixture(api: APIWrapper):
    api.domain.create(CHILD_LIST_DEFINITION)
    created_list = api.domain.get(LISTS_SCHEMA, CHILD_LIST_NAME)
    yield created_list
    # clean up
    api.domain.drop(LISTS_SCHEMA, CHILD_LIST_NAME)


def test_import_rows(api: APIWrapper, parent_list_fixture, child_list_fixture, tmpdir):
    parent_data_path = tmpdir.join("parent_data.csv")
    parent_data_path.write(parent_data)
    child_data_path = tmpdir.join("child_data.csv")
    child_data_path.write(child_data)

    # Should succeed
    parent_file = parent_data_path.open()
    resp = api.query.import_rows(LISTS_SCHEMA, PARENT_LIST_NAME, data_file=parent_file)
    parent_file.close()
    assert resp["success"] == True
    assert resp["rowCount"] == 3

    # Should fail, because data doesn't use rowIds and import_lookup_by_alternate_key defaults to False
    child_file = child_data_path.open()
    resp = api.query.import_rows(LISTS_SCHEMA, CHILD_LIST_NAME, data_file=child_file)
    child_file.close()
    assert resp["success"] == False
    assert resp["errorCount"] == 1
    assert (
        resp["errors"][0]["exception"]
        == "Could not convert value 'parent_one' (String) for Integer field 'parent'"
    )

    # Should pass, because import_lookup_by_alternate_key is True
    child_file = child_data_path.open()
    resp = api.query.import_rows(
        LISTS_SCHEMA, CHILD_LIST_NAME, data_file=child_file, import_lookup_by_alternate_key=True
    )
    child_file.close()
    assert resp["success"] == True
    assert resp["rowCount"] == 3


SAMPLES_SCHEMA = "samples"
BLOOD_SAMPLE_TYPE = "Blood"
TISSUE_SAMPLE_TYPE = "Tissues"


@pytest.fixture
def blood_sample_type_fixture(api: APIWrapper):
    api.domain.create(
        {
            "kind": "SampleSet",
            "domainDesign": {
                "name": BLOOD_SAMPLE_TYPE,
                "description": "Blood samples.",
                "fields": [
                    {"name": "Name", "rangeURI": "string"},
                    {"name": "volume_mL", "rangeURI": "int"},
                    {"name": "DrawDate", "rangeURI": "dateTime"},
                    {"name": "ReceivedDate", "rangeURI": "dateTime"},
                    {"name": "ProblemWithTube", "rangeURI": "boolean"},
                ],
            },
        }
    )
    created_sample_type = api.domain.get(SAMPLES_SCHEMA, BLOOD_SAMPLE_TYPE)
    yield created_sample_type
    # clean up
    api.domain.drop(SAMPLES_SCHEMA, BLOOD_SAMPLE_TYPE)


@pytest.fixture
def tissue_sample_type_fixture(api: APIWrapper):
    api.domain.create(
        {
            "kind": "SampleSet",
            "domainDesign": {
                "name": TISSUE_SAMPLE_TYPE,
                "description": "Tissue samples.",
                "fields": [
                    {"name": "Name", "rangeURI": "string"},
                    {"name": "mass_mg", "rangeURI": "int"},
                    {"name": "ReceivedDate", "rangeURI": "dateTime"},
                ],
            },
        }
    )
    created_sample_type = api.domain.get(SAMPLES_SCHEMA, TISSUE_SAMPLE_TYPE)
    yield created_sample_type
    # clean up
    api.domain.drop(SAMPLES_SCHEMA, TISSUE_SAMPLE_TYPE)


def test_api_save_rows(api: APIWrapper, blood_sample_type_fixture, tissue_sample_type_fixture):
    commands = [
        {
            "command": "insert",
            "schema_name": SAMPLES_SCHEMA,
            "query_name": BLOOD_SAMPLE_TYPE,
            "rows": [{"name": "BL-1"}, {"description": "Should be BL-2 but I forgot to name it"}],
        },
        {
            "command": "insert",
            "schema_name": SAMPLES_SCHEMA,
            "query_name": TISSUE_SAMPLE_TYPE,
            "rows": [{"name": "T-1"}],
        },
    ]

    # Expect to fail this request since the sample name was not specified for one of the rows
    with pytest.raises(ServerContextError) as e:
        api.query.save_rows(commands=commands)
    assert e.value.message == "400: SampleID or Name is required for sample on row 2"

    # Attempt the same request but with a 13.2 api version
    resp = api.query.save_rows(api_version=13.2, commands=commands)
    assert resp["committed"] == False
    assert resp["errorCount"] == 1
    assert (
        resp["result"][0]["errors"]["exception"]
        == "SampleID or Name is required for sample on row 2"
    )

    # Fix the first command by specifying a name for the sample
    commands[0]["rows"][1]["name"] = "BL-2"

    resp = api.query.save_rows(commands=commands)
    assert resp["committed"] == True
    assert resp["errorCount"] == 0
    assert len(resp["result"][0]["rows"]) == 2
    assert len(resp["result"][1]["rows"]) == 1

    first_blood_row_id = resp["result"][0]["rows"][0]["rowid"]
    assert first_blood_row_id > 0

    first_tissue_row_id = resp["result"][1]["rows"][0]["rowid"]
    assert first_tissue_row_id > 0

    # Perform an insert, update, and delete all in the same request
    commands = [
        {
            "command": "insert",
            "schema_name": SAMPLES_SCHEMA,
            "query_name": BLOOD_SAMPLE_TYPE,
            "rows": [
                {"name": "BL-3", "MaterialInputs/Tissues": "T-1"},
                {"name": "BL-4", "MaterialInputs/Blood": "BL-2"},
            ],
        },
        {
            "command": "delete",
            "schema_name": SAMPLES_SCHEMA,
            "query_name": BLOOD_SAMPLE_TYPE,
            "rows": [
                {"rowId": first_blood_row_id},
            ],
        },
        {
            "command": "update",
            "schema_name": SAMPLES_SCHEMA,
            "query_name": TISSUE_SAMPLE_TYPE,
            "rows": [
                {"rowId": first_tissue_row_id, "ReceivedDate": "2025-07-07 12:34:56"},
            ],
        },
    ]

    resp = api.query.save_rows(commands=commands)
    assert resp["committed"] == True
    assert resp["errorCount"] == 0

    # Verify insert
    assert resp["result"][0]["rowsAffected"] == 2
    assert resp["result"][0]["rows"][0]["name"] == "BL-3"
    assert resp["result"][0]["rows"][1]["name"] == "BL-4"

    # Verify delete
    assert resp["result"][1]["rowsAffected"] == 1
    assert resp["result"][1]["rows"][0]["rowid"] == first_blood_row_id

    # Verify update
    assert resp["result"][2]["rowsAffected"] == 1
    assert resp["result"][2]["rows"][0]["rowid"] == first_tissue_row_id
    assert resp["result"][2]["rows"][0]["receiveddate"] == "2025-07-07 12:34:56.000"
