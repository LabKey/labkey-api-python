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


def delete_rows(server_context, schema_name, query_name, rows, container_path=None):
    url = build_url(server_context, 'query', 'deleteRows.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name,
        'rows': rows
    }

    delete_rows_response = _make_request(server_context, url, payload)
    return delete_rows_response


def execute_sql(server_context, schema_name, sql, container_path=None,
                max_rows=None, sort=None, offset=None, container_filter=None):
    url = build_url(server_context, 'query', 'executeSql.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'sql': sql
    }

    if container_filter is not None:
        payload['query.containerFilter'] = container_filter

    if max_rows is not None:
        payload['query.max_rows'] = max_rows

    if offset is not None:
        payload['query.offset'] = offset

    if sort is not None:
        payload['query.sort'] = sort

    execute_sql_response = _make_request(server_context, url, payload)
    return execute_sql_response


def insert_rows(server_context, schema_name, query_name, rows, container_path=None):
    url = build_url(server_context, 'query', 'insertRows.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name,
        'rows': rows
    }

    insert_rows_response = _make_request(server_context, url, payload)
    return insert_rows_response


# TODO: Support all the properties
def select_rows(server_context, schema_name, query_name, view_name=None,
                filter_array=None, container_path=None, columns=None, max_rows=None, sort=None,
                offset=None, container_filter=None):
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
        for filter in filter_array:
            prefix = 'query.' + filter[0] + '~' + filter[1]
            payload[prefix] = filter[2]

    if columns is not None:
        payload['query.columns'] = columns

    if max_rows is not None:
        payload['query.maxRows'] = max_rows

    if sort is not None:
        payload['query.sort'] = sort

    if offset is not None:
        payload['query.offset'] = offset

    if container_filter is not None:
        payload['query.containerFilter'] = container_filter

    select_rows_response = _make_request(server_context, url, payload)
    return select_rows_response


def update_rows(server_context, schema_name, query_name, rows, container_path=None):
    url = build_url(server_context, 'query', 'updateRows.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name,
        'rows': rows
    }

    update_rows_response = _make_request(server_context, url, payload)
    return update_rows_response


def _make_request(server_context, url, payload):
    try:
        session = server_context['session']
        raw_response = session.post(url, headers=_query_headers, data=json.dumps(payload))
        return handle_response(raw_response)
    except SSLError as e:
        raise Exception('Failed to match server SSL configuration. Ensure the server_context is configured correctly.')
