import pytest

from labkey.domain import conditional_format, create, drop, get, save

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
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


@pytest.fixture(scope="function")
def list_fixture(server_context):
    create(server_context, LIST_DEFINITION)
    created_list = get(server_context, LISTS_SCHEMA, LIST_NAME)
    yield created_list
    # clean up
    drop(server_context, LISTS_SCHEMA, LIST_NAME)


def test_add_conditional_format(server_context, list_fixture):
    new_conditional_format = conditional_format(
        query_filter='format.column~lte=7',
        text_color='ff0055',
        background_color='ffffff',
        bold=True,
        italic=False,
        strike_through=False
    )
    for field in list_fixture.fields:
        if field.name == 'formatted':
            field.conditional_formats.append(new_conditional_format)
    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats.__len__() == 2


def test_remove_conditional_format(server_context, list_fixture):
    for field in list_fixture.fields:
        if field.name == 'formatted':
            field.conditional_formats = []
    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats.__len__() == 0
