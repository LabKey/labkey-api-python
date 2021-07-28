import pytest

from labkey.api_wrapper import APIWrapper
from labkey.query import QueryFilter
from labkey.domain import conditional_format

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
LISTS_SCHEMA = "lists"
LIST_NAME = "testlist"
CONDITIONAL_FORMAT = [
    {
        "filter": "format.column~gte=25",
        "textcolor": "ff0000",
        "backgroundcolor": "ffffff",
        "bold": True,
        "italic": False,
        "strikethrough": False,
    }
]
SERIALIZED_QUERY_FILTER = QueryFilter("formatted", 35, QueryFilter.Types.LESS_THAN)
SERIALIZED_CONDITIONAL_FORMAT = conditional_format(
    query_filter=SERIALIZED_QUERY_FILTER, bold=False, text_color="ffff00"
).to_json()
LIST_DEFINITION = {
    "kind": "IntList",
    "domainDesign": {
        "name": LIST_NAME,
        "fields": [
            {"name": "rowId", "rangeURI": "int"},
            {
                "name": "formatted",
                "rangeURI": "int",
                "conditionalFormats": CONDITIONAL_FORMAT,
            },
        ],
    },
    "options": {"keyName": "rowId", "keyType": "AutoIncrementInteger"},
}


@pytest.fixture(scope="function")
def list_fixture(api: APIWrapper):
    api.domain.create(LIST_DEFINITION)
    created_list = api.domain.get(LISTS_SCHEMA, LIST_NAME)
    yield created_list
    # clean up
    api.domain.drop(LISTS_SCHEMA, LIST_NAME)


def test_add_conditional_format(api: APIWrapper, list_fixture):
    new_conditional_format = conditional_format(
        query_filter="format.column~lte=7",
        text_color="ff0055",
        background_color="ffffff",
        bold=True,
        italic=False,
        strike_through=False,
    )

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats.append(new_conditional_format)

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert len(field.conditional_formats) == 2


def test_add_conditional_format_with_multiple_filters(api: APIWrapper, list_fixture):
    new_conditional_formats = [
        conditional_format(
            query_filter=[
                QueryFilter(column="column", value=10, filter_type=QueryFilter.Types.LESS_THAN),
                QueryFilter(
                    column="column",
                    value=100,
                    filter_type=QueryFilter.Types.GREATER_THAN,
                ),
            ],
            text_color="ff0055",
            background_color="ffffff",
            bold=True,
            italic=False,
            strike_through=False,
        )
    ]

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats = []
            field.conditional_formats = new_conditional_formats

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats.__len__() == 1
            assert field.conditional_formats[0].filter == "format.column~lt=10&format.column~gt=100"


@pytest.mark.xfail  # this reproduces https://www.labkey.org/home/Developer/issues/issues-details.view?issueId=41318
def test_add_malformed_query_filter(api: APIWrapper, list_fixture):
    new_conditional_format = conditional_format(
        query_filter="this-is-a-badly-formed-filter",
        text_color="ff0055",
        background_color="ffffff",
        bold=True,
        italic=False,
        strike_through=False,
    )

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats = []
            field.conditional_formats = [new_conditional_format]

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert (
                field.conditional_formats[0].filter != "this-is-a-badly-formed-filter"
            ), "api should discard meaningless filters"


def test_add_conditional_format_with_missing_filter(api: APIWrapper, list_fixture):
    missing_filter_type_filter = QueryFilter("formatted", 13)
    new_conditional_format = conditional_format(
        query_filter=missing_filter_type_filter,
        text_color="ff0055",
        background_color="ffffff",
        bold=True,
        italic=False,
        strike_through=False,
    )

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats = []
            field.conditional_formats = [new_conditional_format]

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats[0].filter == "format.column~eq=13"


def test_remove_conditional_format(api: APIWrapper, list_fixture):
    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats = []

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert len(field.conditional_formats) == 0


def test_update_conditional_format_serialize_filter(api: APIWrapper, list_fixture):
    new_filter = QueryFilter("formatted", 15, QueryFilter.Types.GREATER_THAN_OR_EQUAL)
    cf = conditional_format(new_filter, text_color="ff00ff")

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats[0] = cf

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats[0].filter == "format.column~gte=15"


def test_update_conditional_format_plain_text(api: APIWrapper, list_fixture):
    new_filter = "formatted~gte=15"

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats[0].filter = new_filter

    api.domain.save(LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = api.domain.get(LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats[0].filter == new_filter


def test_create_list_with_conditional_formatted_field(api: APIWrapper):
    composed_list_definition = {
        "kind": "IntList",
        "domainDesign": {
            "name": "composed_list_name",
            "fields": [
                {"name": "rowId", "rangeURI": "int"},
                {
                    "name": "formatted",
                    "rangeURI": "int",
                    "conditionalFormats": [
                        SERIALIZED_CONDITIONAL_FORMAT,
                        {
                            "filter": "format.column~gte=25",
                            "textcolor": "ff0000",
                            "backgroundcolor": "ffffff",
                            "bold": True,
                            "italic": False,
                            "strikethrough": False,
                        },
                    ],
                },
            ],
        },
        "options": {"keyName": "rowId", "keyType": "AutoIncrementInteger"},
    }
    api.domain.create(composed_list_definition)
    created_list = api.domain.get(LISTS_SCHEMA, "composed_list_name")

    for field in created_list.fields:
        if field.name == "formatted":
            assert len(field.conditional_formats) == 2

    api.domain.drop(LISTS_SCHEMA, "composed_list_name")


def test_get_domain_details(api: APIWrapper, list_fixture):
    # test retrieving domain by specifying schema/query
    domain, options = api.domain.get_domain_details(LISTS_SCHEMA, LIST_NAME)
    assert domain.name == LIST_NAME
    assert len(domain.fields) == 2
    assert domain.fields[0].name == "rowId"
    assert domain.fields[1].name == "formatted"
    assert domain.fields[1].conditional_formats[0].to_json() == CONDITIONAL_FORMAT[0]
    assert options["keyName"] == "rowId"
    assert options["name"] == LIST_NAME

    # test retrieving domain by specifying domainId
    assert domain.domain_id is not None
    domain_from_id, domain_from_id_options = api.domain.get_domain_details(
        domain_id=domain.domain_id
    )
    assert domain_from_id.name == LIST_NAME
