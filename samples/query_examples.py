"""
Examples using the Query.py API

Sample data from the New Study tutorial on labkey.org:
    https://www.labkey.org/wiki/home/Documentation/page.view?name=studySetupManual

"""


from __future__ import unicode_literals
from labkey.utils import create_server_context
from labkey.query import select_rows, update_rows, Pagination, QueryFilter, \
    insert_rows, delete_rows, execute_sql
from requests.exceptions import Timeout

import copy

print("Create a server context")
labkey_server = 'localhost:8080'
project_name = 'moduleAssayTest'  # Project folder name
contextPath = 'labkey'
server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=False)

schema = 'lists'
table = 'Demographics'
column1 = 'Group Assignment'
column2 = 'Participant ID'

###################
# Test basic select_rows
###################
result = select_rows(server_context, schema, table)
if result is not None:
    print("select_rows: There are " + str(result['rowCount']) + " rows.")
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)

###################
# Test some parameters of select_rows
###################
result = select_rows(server_context, schema, table,
                     max_rows=5, offset=10, include_total_count=True, include_details_column=True,
                     include_update_column=True, required_version=12.2)
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

