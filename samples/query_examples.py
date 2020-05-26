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
Examples using the Query.py API

Sample data from the New Study tutorial on labkey.org:
    https://www.labkey.org/Documentation/wiki-page.view?name=studySetupManual

"""
from __future__ import unicode_literals

from labkey.utils import create_server_context
from labkey.exceptions import RequestError, QueryNotFoundError, ServerContextError, ServerNotFoundError
from labkey.query import select_rows, update_rows, Pagination, QueryFilter, \
    insert_rows, delete_rows, truncate_table, execute_sql
from requests.exceptions import Timeout

import copy

print("Create a server context")
labkey_server = 'localhost:8080'
project_name = 'ModuleAssayTest'  # Project folder name
context_path = 'labkey'
server_context = create_server_context(labkey_server, project_name, context_path, use_ssl=False)

schema = 'lists'
table = 'Demographics'
column1 = 'Group Assignment'
column2 = 'Participant ID'


###################
# Test basic select_rows
###################
result = select_rows(server_context, schema, table)
if result is not None:
    print(result['rows'][0])
    print("select_rows: There are " + str(result['rowCount']) + " rows.")
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)


###################
# Test error handling
###################
# catch base error
try:
    result = select_rows(server_context, schema, 'badtable')
    print(result)
except RequestError:
    print('Caught base error')

# catch table not found error
try:
    result = select_rows(server_context, schema, 'badtable')
    print(result)
except QueryNotFoundError:
    print('Caught bad table')

# catch schema error
try:
    result = select_rows(server_context, 'badSchema', table)
    print(result)
except QueryNotFoundError:
    print('Caught bad schema')

# catch SSL error
ssl_server_context = create_server_context(labkey_server, project_name, context_path, use_ssl=True)
try:
    result = select_rows(ssl_server_context, schema, table)
    print(result)
except ServerContextError:
    print('Caught SSL Error')


# catch bad context path
bad_server_context = create_server_context(labkey_server, project_name, '', use_ssl=False)
try:
    result = select_rows(bad_server_context, schema, table)
    print(result)
except ServerNotFoundError:
    print('Caught context path')

# catch bad folder path error
bad_server_context = create_server_context(labkey_server, 'bad_project_name', context_path, use_ssl=False)
try:
    result = select_rows(bad_server_context, schema, table)
    print(result)
except ServerNotFoundError:
    print('Caught bad folder name')


###################
# Test some parameters of select_rows
###################
result = select_rows(server_context, schema, table,
                     max_rows=5, offset=10, include_total_count=True, include_details_column=True,
                     include_update_column=True)  # , required_version=12.2)
if result is not None:
    print('select_rows: There are ' + str(len(result['rows'])) + ' rows.')
    print('select_rows: There are ' + str(result['rowCount']) + ' total rows.')
    print('select_rows: Response API version [' + str(result['formatVersion']) + '].')

    column_statement = 'select_rows: Included columns: '
    for column in result['columnModel']:
        column_statement = column_statement + ' ' + column['header'] + ', '
    print(column_statement)

    row = result['rows'][0]
    dataIndex = result['metaData']['id']
    print("select_rows: The first row Key is: " + str(row[dataIndex]))
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)


###################
# Test get all results
###################
result = select_rows(server_context, schema, table, show_rows=Pagination.ALL, include_total_count=True)
if result is not None:
    print("select_rows: There are " + str(len(result['rows'])) + " rows.")
    print('select_rows: There are ' + str(result['rowCount']) + ' total rows.')
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)


###################
# Test sort and select columns
###################
result = select_rows(server_context, schema, table, max_rows=5, offset=10, include_total_count=False,
                     columns=",".join([column1, column2]),
                     sort=column1 + ', -' + column2)  # use '-' to sort descending
if result is not None:
    print('select_rows: There are ' + str(result['rowCount']) + ' rows.')
    print('select_rows: ' + table)
    for row in result['rows']:
        print('\t' + str(row[column1]) + ', ' + str(row[column2]))
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)


###################
# Test basic filters
###################
filters = [
    QueryFilter(column1, 'Group 2: HIV-1 Negative'),
    QueryFilter('Height (inches)', '50, 70', QueryFilter.Types.BETWEEN),
    QueryFilter('Country', 'Germany;Uganda', QueryFilter.Types.IN),
    ]

result = select_rows(server_context, schema, table, filter_array=filters)
if result is not None:
    print("select_rows: There are " + str(result['rowCount']) + " rows.")
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)


###################
# Test update_rows
###################
rows = result['rows']
testRowIdx = 1
originalValue = rows[testRowIdx]
column3 = 'Country'
testRow = {
    'Key': originalValue['Key'],
    column3: 'Pangea'
}

print('update_rows: original value [ ' + originalValue[column3] + ' ]')

updateResult = update_rows(server_context, schema, table, [testRow])
print('update_rows: updated value [ ' + updateResult['rows'][0][column3] + ' ]')

updateResult = update_rows(server_context, schema, table, [originalValue])
print('update_rows: reset value [ ' + updateResult['rows'][0][column3] + ' ]')


###################
# Test insert_rows & delete_rows
###################
testRow = copy.copy(originalValue)

testRow['Key'] = None
testRow['Country'] = 'Antarctica'

all_rows = select_rows(server_context, schema, table)
print('Insert Rows: Initials row count [ ' + str(all_rows['rowCount']) + ' ]')

insertResult = insert_rows(server_context, schema, table, [testRow])
print('Insert Rows: New rowId [ ' + str(insertResult['rows'][0]['Key']) + ' ]')

all_rows = select_rows(server_context, schema, table)
print('Insert Rows: after row count [ ' + str(all_rows['rowCount']) + ' ]')

testRow = insertResult['rows'][0]
deleteResult = delete_rows(server_context, schema, table, [testRow])
print('Delete Rows: deleted rowId [ ' + str(deleteResult['rows'][0]['Key']) + ' ]')

all_rows = select_rows(server_context, schema, table)
print('Delete Rows: after row count [ ' + str(all_rows['rowCount']) + ' ]')


###################
# Test truncate_table
###################
truncate_info = truncate_table(server_context, schema, table)
print('Delete all rows in table: [ ' + str(truncate_info['deletedRows']) + ' ] rows deleted')


###################
# Test execute_sql
###################
sql = 'select * from lists.demographics'

# base execute_sql
sql_result = execute_sql(server_context, schema, sql)
if sql_result is not None:
    print("execute_sql: There are " + str(sql_result['rowCount']) + " rows.")
else:
    print('execute_sql: Failed to load results from ' + schema + '.' + table)

# paging
sql_result = execute_sql(server_context, schema, sql, max_rows=5, offset=10,
                         sort=(column1 + ', -' + column2))
if sql_result is not None:
    print('execute_sql: There are ' + str(len(sql_result['rows'])) + ' rows.')
    print('execute_sql: There are ' + str(sql_result['rowCount']) + ' total rows.')
    print('execute_sql: ' + table)
    for row in sql_result['rows']:
        print('\t' + str(row[column1]) + ', ' + str(row[column2]))
else:
    print('execute_sql: Failed to load results from ' + schema + '.' + table)

# Save query within the session
sql_result = execute_sql(server_context, schema, sql, max_rows=5, offset=10,
                         save_in_session=True)
print('execute_sql: query saved as [ ' + sql_result['queryName'] + ' ]')


# set timeout
try:
    sql_result = execute_sql(server_context, schema, sql, timeout=0.001)
    print('execute_sql did not timeout')
except Timeout:
    print('Caught Timeout')


###################
# Test QC State Definitions
###################

# Create new QC state definitions
qcstates = [{
       'label': 'needs verification',
       'description': 'please look at this',
       'publicData': False
   }, {
       'label': 'approved',
       'publicData': True
}]
result = insert_rows(server_context, 'core', 'qcstate', qcstates)
for row in result['rows']:
    print('Created QC state: ' + row['label'])

result = select_rows(server_context, "core", "qcstate")

# Update a QC state definitions
originalValue = result['rows'][1]
testRow = {
    'RowId': originalValue['RowId'],
    'label': 'Updated Label'
}
updateResult = update_rows(server_context, "core", "qcstate", [testRow])
print('Updated label: approved -> ' + updateResult['rows'][0]['label'])

# Delete all unused QC state definitions
result = select_rows(server_context, 'core', 'qcstate')
for row in result['rows']:
    print('Deleting QC state: ' + row['Label'])
    try:
        delete_rows(server_context, 'core', 'qcstate', [row])
    except ServerContextError as sce:
        print(sce)
