import pytest

from labkey.query import QueryFilter

from labkey.domain import conditional_format, create, drop, get, save

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
def list_fixture(server_context):
    create(server_context, LIST_DEFINITION)
    created_list = get(server_context, LISTS_SCHEMA, LIST_NAME)
    yield created_list
    # clean up
    drop(server_context, LISTS_SCHEMA, LIST_NAME)


def test_add_conditional_format(server_context, list_fixture):
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

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert len(field.conditional_formats) == 2


def test_add_conditional_format_with_multiple_filters(server_context, list_fixture):
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

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats.__len__() == 1
            assert field.conditional_formats[0].filter == "format.column~lt=10&format.column~gt=100"


@pytest.mark.xfail  # this reproduces https://www.labkey.org/home/Developer/issues/issues-details.view?issueId=41318
def test_add_malformed_query_filter(server_context, list_fixture):
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

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert (
                field.conditional_formats[0].filter != "this-is-a-badly-formed-filter"
            ), "api should discard meaningless filters"


def test_add_conditional_format_with_missing_filter(server_context, list_fixture):
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

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats[0].filter == "format.column~eq=13"


def test_remove_conditional_format(server_context, list_fixture):
    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats = []

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert len(field.conditional_formats) == 0


def test_update_conditional_format_serialize_filter(server_context, list_fixture):
    from labkey.query import QueryFilter

    new_filter = QueryFilter("formatted", 15, QueryFilter.Types.GREATER_THAN_OR_EQUAL)
    cf = conditional_format(new_filter, text_color="ff00ff")

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats[0] = cf

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats[0].filter == "format.column~gte=15"


def test_update_conditional_format_plain_text(server_context, list_fixture):
    new_filter = "formatted~gte=15"

    for field in list_fixture.fields:
        if field.name == "formatted":
            field.conditional_formats[0].filter = new_filter

    save(server_context, LISTS_SCHEMA, LIST_NAME, list_fixture)
    saved_domain = get(server_context, LISTS_SCHEMA, LIST_NAME)

    for field in saved_domain.fields:
        if field.name == "formatted":
            assert field.conditional_formats[0].filter == new_filter


def test_create_list_with_conditional_formatted_field(server_context):
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
    create(server_context, composed_list_definition)
    created_list = get(server_context, LISTS_SCHEMA, "composed_list_name")
    for field in created_list.fields:
        if field.name == "formatted":
            assert len(field.conditional_formats) == 2

    drop(server_context, LISTS_SCHEMA, "composed_list_name")
