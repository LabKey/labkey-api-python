#
# Copyright (c) 2015-2026 LabKey Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
############################################################################
NAME:
LabKey Query API

SUMMARY:
This module provides functions for interacting with data on a LabKey Server.

DESCRIPTION:
This module is designed to simplify querying and manipulating data in LabKey Server.
Its APIs are modeled after the LabKey Server JavaScript APIs of the same names.

Installation and Setup for the LabKey Python API:
https://github.com/LabKey/labkey-api-python/blob/master/README.md

Examples of the LabKey Python API:
https://github.com/LabKey/labkey-api-python/tree/master/samples

Documentation for the LabKey Client APIs:
https://www.labkey.org/Documentation/wiki-page.view?name=viewAPIs

Support questions should be directed to the LabKey Developer forum:
https://www.labkey.org/home/developer/forum/project-start.view


############################################################################
"""

import functools
from typing import List, Literal, NotRequired, TextIO, TypedDict

from .server_context import ServerContext
from .utils import json_dumps, waf_encode, transform_options, clean_payload

_default_timeout = 60 * 5  # 5 minutes


class Pagination:
    """
    Enum of paging styles
    """

    PAGINATED = "paginated"
    SELECTED = "selected"
    UNSELECTED = "unselected"
    ALL = "all"
    NONE = "none"


# TODO: Provide filter generators.
#
# There are some inconsistencies between the different filter types with multiple values,
# some use ';' and others use ',' to delimit values within string list; and still others use an array of value objects.
# This is a historical artifact of the api and isn't clearly documented.
#
# https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Filter.html
class QueryFilter:
    """
    Filter object to simplify generation of query filters
    """

    class Types:
        """
        Enumeration of acceptable filter types
        """

        # These operators require a data value
        EQUAL = "eq"
        DATE_EQUAL = "dateeq"

        NEQ = "neq"
        NOT_EQUAL = "neq"
        DATE_NOT_EQUAL = "dateneq"

        NEQ_OR_NULL = "neqornull"
        NOT_EQUAL_OR_MISSING = "neqornull"

        GT = "gt"
        GREATER_THAN = "gt"
        DATE_GREATER_THAN = "dategt"

        LT = "lt"
        LESS_THAN = "lt"
        DATE_LESS_THAN = "datelt"

        GTE = "gte"
        GREATER_THAN_OR_EQUAL = "gte"
        DATE_GREATER_THAN_OR_EQUAL = "dategte"

        LTE = "lte"
        LESS_THAN_OR_EQUAL = "lte"
        DATE_LESS_THAN_OR_EQUAL = "datelte"

        STARTS_WITH = "startswith"
        DOES_NOT_START_WITH = "doesnotstartwith"

        CONTAINS = "contains"
        DOES_NOT_CONTAIN = "doesnotcontain"

        CONTAINS_ONE_OF = "containsoneof"
        CONTAINS_NONE_OF = "containsnoneof"

        ARRAY_CONTAINS_ALL = "arraycontainsall"
        ARRAY_CONTAINS_ANY = "arraycontainsany"
        ARRAY_CONTAINS_NONE = "arraycontainsnone"
        ARRAY_CONTAINS_EXACT = "arraymatches"
        ARRAY_CONTAINS_NOT_EXACT = "arraynotmatches"

        IN = "in"

        EQUALS_ONE_OF = "in"

        NOT_IN = "notin"
        EQUALS_NONE_OF = "notin"

        BETWEEN = "between"
        NOT_BETWEEN = "notbetween"

        MEMBER_OF = "memberof"

        # These are the "no data value" operators
        HAS_ANY_VALUE = ""

        IS_BLANK = "isblank"
        IS_NOT_BLANK = "isnonblank"

        HAS_MISSING_VALUE = "hasmvvalue"
        DOES_NOT_HAVE_MISSING_VALUE = "nomvvalue"

        ARRAY_ISEMPTY = "arrayisempty"
        ARRAY_ISNOTEMPTY = "arrayisnotempty"

        # Table/Query-wise operators
        Q = "q"

        # Ontology operators
        ONTOLOGY_IN_SUBTREE = "concept:insubtree"
        ONTOLOGY_NOT_IN_SUBTREE = "concept:notinsubtree"

        # Lineage operators
        EXP_CHILD_OF = "exp:childof"
        EXP_PARENT_OF = "exp:parentof"
        EXP_LINEAGE_OF = "exp:lineageof"

    def __init__(self, column, value, filter_type=Types.EQUAL):
        self.column_name = column
        self.value = value
        self.filter_type = filter_type

    def get_url_parameter_name(self):
        return "query." + self.column_name + "~" + self.filter_type

    def get_url_parameter_value(self):
        return self.value

    def get_column_name(self):
        return self.column_name

    def __repr__(self):
        return "<QueryFilter [{} {} {}]>".format(self.column_name, self.filter_type, self.value)


class AuditBehavior:
    """
    Enum of different auditing levels
    """

    DETAILED = "DETAILED"
    NONE = "NONE"
    SUMMARY = "SUMMARY"


class InsertOption:
    """
    Enum of the ways import_rows can apply the rows it reads. Not every table supports every option; the server
    rejects an unsupported combination with an error.
    """

    IMPORT = "IMPORT"  # bulk insert, the default for import_rows
    IMPORT_IDENTITY = "IMPORT_IDENTITY"  # bulk insert that preserves the primary keys in the data
    INSERT = "INSERT"  # insert one row at a time, reselecting each inserted row
    MERGE = "MERGE"  # insert new rows, update the columns supplied for rows that already exist
    REPLACE = "REPLACE"  # like MERGE, but nulls the columns of an existing row that the data omits
    UPDATE = "UPDATE"  # update existing rows only, failing if a row does not exist
    UPSERT = "UPSERT"  # like MERGE, but reselects the affected rows


def delete_rows(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    rows: any,
    container_path: str = None,
    transacted: bool = True,
    audit_behavior: AuditBehavior = None,
    audit_user_comment: str = None,
    timeout: int = _default_timeout,
):
    """
    Delete a set of rows from the schema.query
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to delete from
    :param rows: Set of rows to delete
    :param container_path: labkey container path if not already set in context
    :param transacted: whether all of the updates should be done in a single transaction
    :param audit_behavior: used to override the audit behavior for the update. See class query.AuditBehavior
    :param audit_user_comment: used to provide a comment that will be attached to certain detailed audit log records
    :param timeout: timeout of request in seconds (defaults to 300s)
    :return:
    """
    url = server_context.build_url("query", "deleteRows.api", container_path=container_path)

    payload = {"schemaName": schema_name, "queryName": query_name, "rows": rows}

    if transacted is False:
        payload["transacted"] = transacted

    if audit_behavior is not None:
        payload["auditBehavior"] = audit_behavior

    if audit_user_comment is not None:
        payload["auditUserComment"] = audit_user_comment

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


def truncate_table(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    container_path: str = None,
    timeout: int = _default_timeout,
):
    """
    Delete all rows from the schema.query
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to delete from
    :param container_path: labkey container path if not already set in context
    :param timeout: timeout of request in seconds (defaults to 300s)
    :return:
    """
    url = server_context.build_url("query", "truncateTable.api", container_path=container_path)
    payload = {"schemaName": schema_name, "queryName": query_name}

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


def execute_sql(
    server_context: ServerContext,
    schema_name: str,
    sql: str,
    container_path: str = None,
    max_rows: int = None,
    sort: str = None,
    offset: int = None,
    container_filter: str = None,
    save_in_session: bool = None,
    parameters: dict = None,
    required_version: float = None,
    timeout: int = _default_timeout,
    waf_encode_sql: bool = True,
):
    """
    Execute sql query against a LabKey server.

    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param sql: String of labkey sql to execute
    :param container_path: labkey container path if not already set in context
    :param max_rows: max number of rows to return
    :param sort: comma separated list of column names to sort by
    :param offset: number of rows to offset results by
    :param container_filter: enumeration of the various container filters available. See:
        https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Query.html#.containerFilter
    :param save_in_session: save query result as a named view to the session
    :param parameters: parameter values to pass through to a parameterized query
    :param required_version: Api version of response
    :param timeout: timeout of request in seconds (defaults to 300s)
    :param waf_encode_sql: WAF encode sql in request (defaults to True)
    :return:
    """
    url = server_context.build_url("query", "executeSql.api", container_path=container_path)

    payload = clean_payload(
        {
            "schemaName": schema_name,
            "sql": waf_encode(sql) if waf_encode_sql else sql,
            "query.sort": sort,
            "containerFilter": container_filter,
            "maxRows": max_rows,
            "offset": offset,
            "saveInSession": save_in_session,
            "apiVersion": required_version,
        }
    )

    if parameters is not None:
        for key, value in parameters.items():
            payload["query.param." + key] = value

    return server_context.make_request(url, payload, timeout=timeout)


def insert_rows(
    server_context,
    schema_name: str,
    query_name: str,
    rows: List[any],
    container_path: str = None,
    skip_reselect_rows: bool = False,
    transacted: bool = True,
    audit_behavior: AuditBehavior = None,
    audit_user_comment: str = None,
    timeout: int = _default_timeout,
):
    """
    Insert row(s) into table
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to insert into
    :param rows: set of rows to insert
    :param container_path: labkey container path if not already set in context
    :param skip_reselect_rows: whether the full detailed response for the insert can be skipped
    :param transacted: whether all of the updates should be done in a single transaction
    :param audit_behavior: used to override the audit behavior for the update. See class query.AuditBehavior
    :param audit_user_comment: used to provide a comment that will be attached to certain detailed audit log records
    :param timeout: timeout of request in seconds (defaults to 300s)
    :return:
    """
    url = server_context.build_url("query", "insertRows.api", container_path=container_path)

    payload = {"schemaName": schema_name, "queryName": query_name, "rows": rows}

    if skip_reselect_rows is True:
        payload["skipReselectRows"] = skip_reselect_rows

    if transacted is False:
        payload["transacted"] = transacted

    if audit_behavior is not None:
        payload["auditBehavior"] = audit_behavior

    if audit_user_comment is not None:
        payload["auditUserComment"] = audit_user_comment

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


def import_rows(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    data_file: TextIO = None,
    container_path: str = None,
    insert_option: InsertOption = None,
    audit_behavior: AuditBehavior = None,
    import_lookup_by_alternate_key: bool = None,
    timeout: int = _default_timeout,
    audit_details: dict = None,
    audit_user_comment: str = None,
    format: Literal["csv", "tsv"] = None,
    import_identity: bool = None,
    import_url: str = None,
    module: str = None,
    module_resource: str = None,
    path: str = None,
    save_to_pipeline: bool = None,
    text: str = None,
    use_async: bool = None,
):
    """
    Import row(s) into a table.

    The rows may come from one of four sources, and the server uses the first one supplied in this order: text, path,
    module_resource, data_file. Supplying more than one silently ignores the others. The column names in the data must
    match the column names from the LabKey server.

    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to import into
    :param data_file: an open file object holding the rows to import, uploaded as multipart form data
    :param container_path: labkey container path if not already set in context
    :param insert_option: How the rows are applied. See class query.InsertOption. Defaults to "IMPORT", a bulk insert
    that creates a new row for each row of data. "MERGE" instead updates the rows that already exist and inserts the
    rest; when merging you only need to provide the columns you wish to update, existing data for other columns will
    be left as is.
    :param audit_behavior: Set the level of auditing details for this import action. Available options are "SUMMARY" and
    "DETAILED". SUMMARY - Audit log reflects that a change was made, but does not mention the nature of the change.
    DETAILED - Provides full details on what change was made, including values before and after the change. Defaults to
    the setting as specified by the LabKey query.
    :param import_lookup_by_alternate_key: Allows lookup target rows to be resolved by values rather than the target's
    primary key. This option will only be available for lookups that are configured with unique column information.
    Defaults to False.
    :param timeout: Request timeout in seconds (defaults to 300s)
    :param audit_details: Additional detail to record on the transaction audit event for this import, serialized to
    JSON for the request. Keys are matched case insensitively against the server's transaction detail names
    ("Product", "EditMethod", "RequestSource", etc.); unrecognized keys are ignored.
    :param audit_user_comment: used to provide a comment that will be attached to certain detailed audit log records
    :param format: Delimiter of the text option, either "csv" or "tsv". Defaults to "tsv". Ignored by the other
    sources, whose format is determined by the file itself.
    :param import_identity: Insert the primary key values present in the data rather than letting the server assign
    them. Requires an administrator, and is only supported for tables with an auto incrementing primary key.
    :param import_url: Full URL of an alternate import action to post to, replacing the default query-import.api. Use
    it to reach an import action of another controller that accepts the same parameters.
    :param module: Name of the module to resolve module_resource against. Defaults to the module owning the target
    table's schema. Only used together with module_resource.
    :param module_resource: Path of a TSV resource within the module to import, relative to the module root. A value
    with no "/" is resolved under the module's "schemas/dbscripts" directory.
    :param path: Path of a file already on the server to import, resolved against the WebDAV root (for example
    "_webdav/MyProject/@files/data.tsv"). The current user must be able to read it.
    :param save_to_pipeline: Copy the uploaded file into a QueryImportFiles directory under the container's pipeline
    root instead of discarding it once the import completes. Requires a pipeline root. Defaults to False.
    :param text: The rows to import, as inline delimited text, including the header row. See the format option.
    :param use_async: Run the import in a background pipeline job, which also saves the file to the pipeline root.
    The response holds "jobId" rather than a row count, and not every table supports it. Defaults to False.
    :return:
    """
    url = import_url or server_context.build_url(
        "query", "import.api", container_path=container_path
    )
    file_payload = {"file": data_file} if data_file is not None else None
    # every option the server accepts, omitted from the request when left unset
    payload = clean_payload(
        {
            "auditBehavior": audit_behavior,
            "auditDetails": None if audit_details is None else json_dumps(audit_details),
            "auditUserComment": audit_user_comment,
            "format": format,
            "importIdentity": import_identity,
            "importLookupByAlternateKey": import_lookup_by_alternate_key,
            "insertOption": insert_option,
            "module": module,
            "moduleResource": module_resource,
            "path": path,
            "saveToPipeline": save_to_pipeline,
            "queryName": query_name,
            "schemaName": schema_name,
            "text": text,
            "useAsync": use_async,
        }
    )

    return server_context.make_request(
        url, payload, method="POST", file_payload=file_payload, timeout=timeout
    )


command_option_fields = [
    "audit_behavior",
    "audit_user_comment",
    "container_path",
    "extra_context",
    "skip_reselect_rows",
]


class Command(TypedDict):
    """
    TypedDict representing a command for saveRows API.
    """

    audit_behavior: NotRequired[AuditBehavior]
    audit_user_comment: NotRequired[str]
    command: Literal["insert", "update", "delete"]
    container_path: NotRequired[str]
    extra_context: NotRequired[dict]
    query_name: str
    rows: List[any]
    schema_name: str
    skip_reselect_rows: NotRequired[bool]


def save_rows(
    server_context: ServerContext,
    commands: List[Command],
    api_version: float = None,
    container_path: str = None,
    extra_context: dict = None,
    timeout: int = _default_timeout,
    transacted: bool = None,
    validate_only: bool = None,
):
    """
    Save inserts, updates, and/or deletes to potentially multiple tables with a single request.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param commands: A List of the update/insert/delete operations to be performed.
    :param api_version: decimal value that indicates the response version of the api. If this is 13.2 or higher, a
    request that fails validation will be returned as a successful response. Use the 'errorCount' and 'committed'
    properties in the response to tell if it committed or not.
    :param container_path: folder path if not already part of server_context
    :param extra_context: Extra context object passed into the transformation/validation script environment.
    :param timeout: Request timeout in seconds (defaults to 300s)
    :param transacted: Whether all the commands should be done in a single transaction, so they all succeed or all
    fail. Defaults to true.
    :param validate_only: Whether the server should attempt to proceed through all the commands but not commit them to
    the database. Useful for scenarios like giving incremental validation feedback as a user fills out a UI form but
    does not save anything until they explicitly request a save.
    """
    url = server_context.build_url("query", "saveRows.api", container_path=container_path)

    # the required keys are read directly so a malformed Command still raises a KeyError naming it
    json_commands = [
        {
            "command": command["command"],
            "queryName": command["query_name"],
            "schemaName": command["schema_name"],
            "rows": command["rows"],
            **clean_payload(transform_options(command, command_option_fields)),
        }
        for command in commands
    ]

    payload = clean_payload(
        {
            "commands": json_commands,
            "apiVersion": api_version,
            "extraContext": extra_context,
            "transacted": transacted,
            "validateOnly": validate_only,
        }
    )

    return server_context.make_request(url, json=payload, timeout=timeout)


def select_rows(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    view_name: str = None,
    filter_array: List[QueryFilter] = None,
    container_path: str = None,
    columns=None,
    max_rows: int = -1,
    sort: str = None,
    offset: int = None,
    container_filter: str = None,
    parameters: dict = None,
    show_rows: bool = None,
    include_total_count: bool = None,
    include_details_column: bool = None,
    include_update_column: bool = None,
    selection_key: str = None,
    required_version: float = None,
    timeout: int = _default_timeout,
    ignore_filter: bool = None,
):
    """
    Query data from a LabKey server
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to select from
    :param view_name: pre-existing named view
    :param filter_array: set of filter objects to apply
    :param container_path: folder path if not already part of server_context
    :param columns: set of columns to retrieve
    :param max_rows: max number of rows to retrieve, defaults to -1 (unlimited)
    :param sort: comma separated list of column names to sort by, prefix a column with '-' to sort descending
    :param offset: number of rows to offset results by
    :param container_filter: enumeration of the various container filters available. See:
        https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Query.html#.containerFilter
    :param parameters: Set of parameters to pass along to a parameterized query
    :param show_rows: An enumeration of various paging styles
    :param include_total_count: Boolean value that indicates whether to include a total count value in response
    :param include_details_column: Boolean value that indicates whether to include a Details link column in results
    :param include_update_column: Boolean value that indicates whether to include an Update link column in results
    :param selection_key:
    :param required_version: decimal value that indicates the response version of the api
    :param timeout: Request timeout in seconds (defaults to 300s)
    :param ignore_filter: Boolean, if true, the command will ignore any filter that may be part of the chosen view.
    :return:
    """
    url = server_context.build_url("query", "getQuery.api", container_path=container_path)
    payload = clean_payload(
        {
            "schemaName": schema_name,
            "query.queryName": query_name,
            "query.viewName": view_name,
            "query.columns": columns,
            "query.maxRows": max_rows,
            "query.sort": sort,
            "query.offset": offset,
            "query.showRows": show_rows,
            "query.selectionKey": selection_key,
            "query.ignoreFilter": 1 if ignore_filter else None,
            "containerFilter": container_filter,
            "includeTotalCount": include_total_count,
            "includeDetailsColumn": include_details_column,
            "includeUpdateColumn": include_update_column,
            "apiVersion": required_version,
        }
    )

    if filter_array is not None:
        for query_filter in filter_array:
            prefix = query_filter.get_url_parameter_name()
            # Use a list for each prefix, as a prefix may have multiple different
            # filter values associated for it.
            filters = payload.get(prefix, [])
            filters.append(query_filter.get_url_parameter_value())
            payload[prefix] = filters

    if parameters is not None:
        for key, value in parameters.items():
            payload["query.param." + key] = value

    return server_context.make_request(url, payload, timeout=timeout)


def update_rows(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    rows: List[any],
    container_path: str = None,
    transacted: bool = True,
    audit_behavior: AuditBehavior = None,
    audit_user_comment: str = None,
    timeout: int = _default_timeout,
):
    """
    Update a set of rows

    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to update
    :param rows: Set of rows to update
    :param container_path: labkey container path if not already set in context
    :param transacted: whether all of the updates should be done in a single transaction
    :param audit_behavior: used to override the audit behavior for the update. See class query.AuditBehavior
    :param audit_user_comment: used to provide a comment that will be attached to certain detailed audit log records
    :param timeout: timeout of request in seconds (defaults to 300s)
    :return:
    """
    url = server_context.build_url("query", "updateRows.api", container_path=container_path)

    payload = {"schemaName": schema_name, "queryName": query_name, "rows": rows}

    if transacted is False:
        payload["transacted"] = transacted

    if audit_behavior is not None:
        payload["auditBehavior"] = audit_behavior

    if audit_user_comment is not None:
        payload["auditUserComment"] = audit_user_comment

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


def move_rows(
    server_context: ServerContext,
    target_container_path: str,
    schema_name: str,
    query_name: str,
    rows: any,
    container_path: str = None,
    transacted: bool = True,
    audit_behavior: AuditBehavior = None,
    audit_user_comment: str = None,
    timeout: int = _default_timeout,
):
    """
    Move a set of rows from the schema.query
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param target_container_path: target labkey container path for the move
    :param schema_name: schema of table
    :param query_name: table name to move from
    :param rows: Set of rows to move
    :param container_path: source labkey container path if not already set in context
    :param transacted: whether all of the updates should be done in a single transaction
    :param audit_behavior: used to override the audit behavior for the update. See class query.AuditBehavior
    :param audit_user_comment: used to provide a comment that will be attached to certain detailed audit log records
    :param timeout: timeout of request in seconds (defaults to 300s)
    :return:
    """
    url = server_context.build_url("query", "moveRows.api", container_path=container_path)

    payload = {
        "targetContainerPath": target_container_path,
        "schemaName": schema_name,
        "queryName": query_name,
        "rows": rows,
    }

    if transacted is False:
        payload["transacted"] = transacted

    if audit_behavior is not None:
        payload["auditBehavior"] = audit_behavior

    if audit_user_comment is not None:
        payload["auditUserComment"] = audit_user_comment

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


get_queries_fields = [
    "schema_name",
    "include_columns",
    "include_system_queries",
    "include_title",
    "include_user_queries",
    "include_view_data_url",
    "query_detail_columns",
]


def get_queries(
    server_context: ServerContext,
    schema_name: str,
    container_path: str = None,
    timeout=_default_timeout,
    **kwargs,
) -> dict:
    """
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param container_path: folder path if not already part of server_context
    :param timeout: Request timeout in seconds (defaults to 300s)
    :param kwargs: Optional parameters supported by this API:
        include_columns: boolean, if set to False, information about the available columns in this query will not be
            included in the results. Default is True.
        include_system_queries: boolean, if set to false, system-defined queries will not be included in the results.
            Default is True.
        include_title: boolean, if set to False, no custom query titles will be included. Instead, titles will be
            identical to names. Default is True.
        include_user_queries: boolean, if set to False, user-defined queries will not be included in the results.
            Default is True.
        include_view_data_url: boolean, if set to False, view data URLs will not be included in the results.
            Default is True.
        query_detail_columns: boolean, if set to True, and includeColumns is set to True, information about the
            available columns will be the same details as specified by getQueryDetails for columns. Defaults to False.
    :return: dict
    """
    url = server_context.build_url("query", "getQueries.api", container_path=container_path)
    payload = {"schemaName": schema_name}

    if len(kwargs) > 0:
        payload = {**payload, **transform_options(kwargs, get_queries_fields)}

    return server_context.make_request(url, payload, timeout=timeout)


class QueryWrapper:
    """
    Wrapper for all of the API methods exposed in the query module. Used by the APIWrapper class.
    """

    def __init__(self, server_context: ServerContext):
        self.server_context = server_context

    @functools.wraps(delete_rows)
    def delete_rows(
        self,
        schema_name: str,
        query_name: str,
        rows: any,
        container_path: str = None,
        transacted: bool = True,
        audit_behavior: AuditBehavior = None,
        audit_user_comment: str = None,
        timeout: int = _default_timeout,
    ):
        return delete_rows(
            self.server_context,
            schema_name,
            query_name,
            rows,
            container_path,
            transacted,
            audit_behavior,
            audit_user_comment,
            timeout,
        )

    @functools.wraps(truncate_table)
    def truncate_table(
        self, schema_name, query_name, container_path=None, timeout=_default_timeout
    ):
        return truncate_table(self.server_context, schema_name, query_name, container_path, timeout)

    @functools.wraps(execute_sql)
    def execute_sql(
        self,
        schema_name: str,
        sql: str,
        container_path: str = None,
        max_rows: int = None,
        sort: str = None,
        offset: int = None,
        container_filter: str = None,
        save_in_session: bool = None,
        parameters: dict = None,
        required_version: float = None,
        timeout: int = _default_timeout,
        waf_encode_sql: bool = True,
    ):
        return execute_sql(
            self.server_context,
            schema_name,
            sql,
            container_path,
            max_rows,
            sort,
            offset,
            container_filter,
            save_in_session,
            parameters,
            required_version,
            timeout,
            waf_encode_sql,
        )

    @functools.wraps(insert_rows)
    def insert_rows(
        self,
        schema_name: str,
        query_name: str,
        rows: List[any],
        container_path: str = None,
        skip_reselect_rows: bool = False,
        transacted: bool = True,
        audit_behavior: AuditBehavior = None,
        audit_user_comment: str = None,
        timeout: int = _default_timeout,
    ):
        return insert_rows(
            self.server_context,
            schema_name,
            query_name,
            rows,
            container_path,
            skip_reselect_rows,
            transacted,
            audit_behavior,
            audit_user_comment,
            timeout,
        )

    @functools.wraps(import_rows)
    def import_rows(
        self,
        schema_name: str,
        query_name: str,
        data_file: TextIO = None,
        container_path: str = None,
        insert_option: InsertOption = None,
        audit_behavior: AuditBehavior = None,
        import_lookup_by_alternate_key: bool = None,
        timeout: int = _default_timeout,
        audit_details: dict = None,
        audit_user_comment: str = None,
        format: Literal["csv", "tsv"] = None,
        import_identity: bool = None,
        import_url: str = None,
        module: str = None,
        module_resource: str = None,
        path: str = None,
        save_to_pipeline: bool = None,
        text: str = None,
        use_async: bool = None,
    ):
        return import_rows(
            self.server_context,
            schema_name,
            query_name,
            data_file,
            container_path,
            insert_option,
            audit_behavior,
            import_lookup_by_alternate_key,
            timeout,
            audit_details,
            audit_user_comment,
            format,
            import_identity,
            import_url,
            module,
            module_resource,
            path,
            save_to_pipeline,
            text,
            use_async,
        )

    @functools.wraps(save_rows)
    def save_rows(
        self,
        commands: List[Command],
        api_version: float = None,
        container_path: str = None,
        extra_context: dict = None,
        timeout: int = _default_timeout,
        transacted: bool = None,
        validate_only: bool = None,
    ):
        return save_rows(
            self.server_context,
            commands,
            api_version,
            container_path,
            extra_context,
            timeout,
            transacted,
            validate_only,
        )

    @functools.wraps(select_rows)
    def select_rows(
        self,
        schema_name: str,
        query_name: str,
        view_name: str = None,
        filter_array: List[QueryFilter] = None,
        container_path: str = None,
        columns=None,
        max_rows: int = -1,
        sort: str = None,
        offset: int = None,
        container_filter: str = None,
        parameters: dict = None,
        show_rows: bool = None,
        include_total_count: bool = None,
        include_details_column: bool = None,
        include_update_column: bool = None,
        selection_key: str = None,
        required_version: float = None,
        timeout: int = _default_timeout,
        ignore_filter: bool = None,
    ):
        return select_rows(
            self.server_context,
            schema_name,
            query_name,
            view_name,
            filter_array,
            container_path,
            columns,
            max_rows,
            sort,
            offset,
            container_filter,
            parameters,
            show_rows,
            include_total_count,
            include_details_column,
            include_update_column,
            selection_key,
            required_version,
            timeout,
            ignore_filter,
        )

    @functools.wraps(update_rows)
    def update_rows(
        self,
        schema_name: str,
        query_name: str,
        rows: List[any],
        container_path: str = None,
        transacted: bool = True,
        audit_behavior: AuditBehavior = None,
        audit_user_comment: str = None,
        timeout: int = _default_timeout,
    ):
        return update_rows(
            self.server_context,
            schema_name,
            query_name,
            rows,
            container_path,
            transacted,
            audit_behavior,
            audit_user_comment,
            timeout,
        )

    @functools.wraps(move_rows)
    def move_rows(
        self,
        target_container_path: str,
        schema_name: str,
        query_name: str,
        rows: any,
        container_path: str = None,
        transacted: bool = True,
        audit_behavior: AuditBehavior = None,
        audit_user_comment: str = None,
        timeout: int = _default_timeout,
    ):
        return move_rows(
            self.server_context,
            target_container_path,
            schema_name,
            query_name,
            rows,
            container_path,
            transacted,
            audit_behavior,
            audit_user_comment,
            timeout,
        )

    @functools.wraps(get_queries)
    def get_queries(
        self,
        schema_name: str,
        container_path: str = None,
        include_columns: bool = None,
        include_system_queries: bool = None,
        include_title: bool = None,
        include_user_queries: bool = None,
        include_view_data_url: bool = None,
        query_detail_columns: bool = None,
        timeout=_default_timeout,
    ):
        return get_queries(
            self.server_context,
            schema_name,
            container_path,
            timeout,
            include_columns=include_columns,
            include_system_queries=include_system_queries,
            include_title=include_title,
            include_user_queries=include_user_queries,
            include_view_data_url=include_view_data_url,
            query_detail_columns=query_detail_columns,
        )
