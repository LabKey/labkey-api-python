#
# Copyright (c) 2011-2015 LabKey Corporation
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

Documentation:
LabKey Python API:
https://www.labkey.org/wiki/home/Documentation/page.view?name=python

Setup, configuration of the LabKey Python API:
https://www.labkey.org/wiki/home/Documentation/page.view?name=setupPython

Using the LabKey Python API:
https://www.labkey.org/wiki/home/Documentation/page.view?name=usingPython

Documentation for the LabKey client APIs:
https://www.labkey.org/wiki/home/Documentation/page.view?name=viewAPIs

Support questions should be directed to the LabKey forum:
https://www.labkey.org/announcements/home/Server/Forum/list.view?


############################################################################
"""
from __future__ import unicode_literals
import json

from requests.exceptions import SSLError
from labkey.utils import build_url, handle_response


_query_headers = {
    'Content-Type': 'application/json'
}

_default_timeout = 30  # in seconds


class Pagination:
    PAGINATED = 'paginated'
    SELECTED = 'selected'
    UNSELECTED = 'unselected'
    ALL = 'all'
    NONE = 'none'


def delete_rows(server_context, schema_name, query_name, rows, container_path=None, transacted=None, timeout=_default_timeout):
    url = build_url(server_context, 'query', 'deleteRows.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name,
        'rows': rows
    }

    # explicit json payload and headers required for form generation
    delete_rows_response = _make_request(server_context, url, json.dumps(payload), headers=_query_headers, timeout=timeout)
    return delete_rows_response


def execute_sql(server_context, schema_name, sql, container_path=None,
                max_rows=None,
                sort=None,
                offset=None,
                container_filter=None,
                save_in_session=None,
                parameters=None,
                required_version=None,
                timeout=_default_timeout):
    url = build_url(server_context, 'query', 'executeSql.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'sql': sql
    }

    if container_filter is not None:
        payload['containerFilter'] = container_filter

    if max_rows is not None:
        payload['maxRows'] = max_rows

    if offset is not None:
        payload['offset'] = offset

    if sort is not None:
        payload['query.sort'] = sort

    if save_in_session is not None:
        payload['saveInSession'] = save_in_session

    if parameters is not None:
        payload['query.parameters'] = parameters

    if required_version is not None:
        payload['apiVersion'] = required_version

    execute_sql_response = _make_request(server_context, url, payload, timeout=timeout)
    return execute_sql_response


def insert_rows(server_context, schema_name, query_name, rows, container_path=None, timeout=_default_timeout):
    url = build_url(server_context, 'query', 'insertRows.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name,
        'rows': rows
    }

    # explicit json payload and headers required for form generation
    insert_rows_response = _make_request(server_context, url, json.dumps(payload), headers=_query_headers, timeout=timeout)
    return insert_rows_response


def select_rows(server_context, schema_name, query_name, view_name=None,
                filter_array=None,
                container_path=None,
                columns=None,
                max_rows=None,
                sort=None,
                offset=None,
                container_filter=None,
                parameters=None,
                show_rows=None,
                include_total_count=None,
                include_details_column=None,
                include_update_column=None,
                selection_key=None,
                required_version=None,
                timeout=_default_timeout
                ):
    # TODO: Support data_region_name
    url = build_url(server_context, 'query', 'getQuery.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'query.queryName': query_name
    }

    # TODO: Roll these checks up
    if view_name is not None:
        payload['query.viewName'] = view_name

    if filter_array is not None:
        for query_filter in filter_array:
            prefix = query_filter.get_url_parameter_name()
            payload[prefix] = query_filter.get_url_parameter_value()

    if columns is not None:
        payload['query.columns'] = columns

    if max_rows is not None:
        payload['query.maxRows'] = max_rows

    if sort is not None:
        payload['query.sort'] = sort

    if offset is not None:
        payload['query.offset'] = offset

    if container_filter is not None:
        payload['containerFilter'] = container_filter

    if parameters is not None:
        payload['query.parameters'] = parameters

    if show_rows is not None:
        payload['query.showRows'] = show_rows

    if include_total_count is not None:
        payload['includeTotalCount'] = include_total_count

    if include_details_column is not None:
        payload['includeDetailsColumn'] = include_details_column

    if include_update_column is not None:
        payload['includeUpdateColumn'] = include_update_column

    if selection_key is not None:
        payload['query.selectionKey'] = selection_key

    if required_version is not None:
        payload['apiVersion'] = required_version

    select_rows_response = _make_request(server_context, url, payload, timeout=timeout)
    return select_rows_response


def update_rows(server_context, schema_name, query_name, rows, container_path=None, timeout=_default_timeout):
    url = build_url(server_context, 'query', 'updateRows.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name,
        'rows': rows
    }

    # explicit json payload and headers required for form generation
    update_rows_response = _make_request(server_context, url, json.dumps(payload), headers=_query_headers, timeout=timeout)
    return update_rows_response


def _make_request(server_context, url, payload, headers=None, timeout=_default_timeout):
    try:
        session = server_context['session']
        raw_response = session.post(url, data=payload, headers=headers, timeout=timeout)
        return handle_response(raw_response)
    except SSLError as e:
        raise Exception('Failed to match server SSL configuration. Ensure the server_context is configured correctly.')


# TODO: Provide filter generators.
#
# There are some inconsistencies between the different filter types with multiple values,
# some use ';' and others use ',' to delimit values within string list; and still others use an array of value objects.
# This is a historical artifact of the api and isn't clearly documented.
#
# https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Filter.html
class QueryFilter:

    class Types:
        HAS_ANY_VALUE = '',

        EQUAL = 'eq',
        DATE_EQUAL = 'dateeq',

        NEQ = 'neq',
        NOT_EQUAL = 'neq',
        DATE_NOT_EQUAL = 'dateneq',

        NEQ_OR_NULL = 'neqornull',
        NOT_EQUAL_OR_MISSING = 'neqornull',

        GT = 'gt',
        GREATER_THAN = 'gt',
        DATE_GREATER_THAN = 'dategt',

        LT = 'lt',
        LESS_THAN = 'lt',
        DATE_LESS_THAN = 'datelt',

        GTE = 'gte',
        GREATER_THAN_OR_EQUAL = 'gte',
        DATE_GREATER_THAN_OR_EQUAL = 'dategte',

        LTE = 'lte',
        LESS_THAN_OR_EQUAL = 'lte',
        DATE_LESS_THAN_OR_EQUAL = 'datelte',

        STARTS_WITH = 'startswith',
        DOES_NOT_START_WITH = 'doesnotstartwith',

        CONTAINS = 'contains',
        DOES_NOT_CONTAIN = 'doesnotcontain',

        CONTAINS_ONE_OF = 'containsoneof',
        CONTAINS_NONE_OF = 'containsnoneof',

        IN = 'in',

        EQUALS_ONE_OF = 'in',

        NOT_IN = 'notin',
        EQUALS_NONE_OF = 'notin',

        BETWEEN = 'between',
        NOT_BETWEEN = 'notbetween',

        MEMBER_OF = 'memberof'

    def __init__(self, column, value, filter_type = Types.EQUAL):
        self.column_name = column
        self.value = value
        self.filter_type = filter_type

    def get_url_parameter_name(self):
        return 'query.' + self.column_name + '~' + self.filter_type[0]

    def get_url_parameter_value(self):
        return self.value

    def get_column_name(self):
        return self.column_name

