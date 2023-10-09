#
# Copyright (c) 2015-2018 LabKey Corporation
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
from typing import List

from .server_context import ServerContext

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


def delete_rows(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    rows: any,
    container_path: str = None,
    timeout: int = _default_timeout,
):
    """
    Delete a set of rows from the schema.query
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to delete from
    :param rows: Set of rows to delete
    :param container_path: labkey container path if not already set in context
    :param timeout: timeout of request in seconds (defaults to 30s)
    :return:
    """
    url = server_context.build_url("query", "deleteRows.api", container_path=container_path)
    payload = {"schemaName": schema_name, "queryName": query_name, "rows": rows}

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
    :param timeout: timeout of request in seconds (defaults to 30s)
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
    :param timeout: timeout of request in seconds (defaults to 30s)
    :return:
    """
    url = server_context.build_url("query", "executeSql.api", container_path=container_path)

    payload = {"schemaName": schema_name, "sql": sql}

    if container_filter is not None:
        payload["containerFilter"] = container_filter

    if max_rows is not None:
        payload["maxRows"] = max_rows

    if offset is not None:
        payload["offset"] = offset

    if sort is not None:
        payload["query.sort"] = sort

    if save_in_session is not None:
        payload["saveInSession"] = save_in_session

    if parameters is not None:
        for key, value in parameters.items():
            payload["query.param." + key] = value

    if required_version is not None:
        payload["apiVersion"] = required_version

    return server_context.make_request(url, payload, timeout=timeout)


def insert_rows(
    server_context,
    schema_name: str,
    query_name: str,
    rows: List[any],
    container_path: str = None,
    timeout: int = _default_timeout,
):
    """
    Insert row(s) into table
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to insert into
    :param rows: set of rows to insert
    :param container_path: labkey container path if not already set in context
    :param timeout: timeout of request in seconds (defaults to 30s)
    :return:
    """
    url = server_context.build_url("query", "insertRows.api", container_path=container_path)

    payload = {"schemaName": schema_name, "queryName": query_name, "rows": rows}

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


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
    :param timeout: Request timeout in seconds (defaults to 30s)
    :param ignore_filter: Boolean, if true, the command will ignore any filter that may be part of the chosen view.
    :return:
    """
    url = server_context.build_url("query", "getQuery.api", container_path=container_path)
    payload = {"schemaName": schema_name, "query.queryName": query_name}

    if view_name is not None:
        payload["query.viewName"] = view_name

    if filter_array is not None:
        for query_filter in filter_array:
            prefix = query_filter.get_url_parameter_name()
            # Use a list for each prefix, as a prefix may have multiple different
            # filter values associated for it.
            filters = payload.get(prefix, [])
            filters.append(query_filter.get_url_parameter_value())
            payload[prefix] = filters

    if columns is not None:
        payload["query.columns"] = columns

    if max_rows is not None:
        payload["query.maxRows"] = max_rows

    if sort is not None:
        payload["query.sort"] = sort

    if offset is not None:
        payload["query.offset"] = offset

    if container_filter is not None:
        payload["containerFilter"] = container_filter

    if parameters is not None:
        for key, value in parameters.items():
            payload["query.param." + key] = value

    if show_rows is not None:
        payload["query.showRows"] = show_rows

    if include_total_count is not None:
        payload["includeTotalCount"] = include_total_count

    if include_details_column is not None:
        payload["includeDetailsColumn"] = include_details_column

    if include_update_column is not None:
        payload["includeUpdateColumn"] = include_update_column

    if selection_key is not None:
        payload["query.selectionKey"] = selection_key

    if required_version is not None:
        payload["apiVersion"] = required_version

    if ignore_filter is not None and ignore_filter is True:
        payload["query.ignoreFilter"] = 1

    return server_context.make_request(url, payload, timeout=timeout)


def update_rows(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    rows: List[any],
    container_path: str = None,
    timeout: int = _default_timeout,
):
    """
    Update a set of rows

    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name to update
    :param rows: Set of rows to update
    :param container_path: labkey container path if not already set in context
    :param timeout: timeout of request in seconds (defaults to 30s)
    :return:
    """
    url = server_context.build_url("query", "updateRows.api", container_path=container_path)

    payload = {"schemaName": schema_name, "queryName": query_name, "rows": rows}

    return server_context.make_request(
        url,
        json=payload,
        timeout=timeout,
    )


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
        timeout: int = _default_timeout,
    ):
        return delete_rows(
            self.server_context, schema_name, query_name, rows, container_path, timeout
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
        )

    @functools.wraps(insert_rows)
    def insert_rows(
        self,
        schema_name: str,
        query_name: str,
        rows: List[any],
        container_path: str = None,
        timeout: int = _default_timeout,
    ):
        return insert_rows(
            self.server_context, schema_name, query_name, rows, container_path, timeout
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
        timeout: int = _default_timeout,
    ):
        return update_rows(
            self.server_context, schema_name, query_name, rows, container_path, timeout
        )
