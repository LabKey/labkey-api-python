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
from labkey.api_wrapper import APIWrapper
from labkey.exceptions import (
    RequestError,
    QueryNotFoundError,
    ServerContextError,
    ServerNotFoundError,
)
from labkey.query import Pagination, QueryFilter
from requests.exceptions import Timeout

import copy

print("Create a server context")
labkey_server = "localhost:8080"
project_name = "ModuleAssayTest"  # Project folder name
context_path = "labkey"
api = APIWrapper(labkey_server, project_name, context_path, use_ssl=False)

schema = "lists"
table = "Demographics"
column1 = "Group Assignment"
column2 = "Participant ID"


###################
# Test basic select_rows
###################
result = api.query.select_rows(schema, table)
if result is not None:
    print(result["rows"][0])
    print("select_rows: There are " + str(result["rowCount"]) + " rows.")
else:
    print("select_rows: Failed to load results from " + schema + "." + table)


###################
# Test error handling
###################
# catch base error
try:
    result = api.query.select_rows(schema, "badtable")
    print(result)
except RequestError:
    print("Caught base error")

# catch table not found error
try:
    result = api.query.select_rows(schema, "badtable")
    print(result)
except QueryNotFoundError:
    print("Caught bad table")

# catch schema error
try:
    result = api.query.select_rows("badSchema", table)
    print(result)
except QueryNotFoundError:
    print("Caught bad schema")

# catch SSL error
ssl_api = APIWrapper(labkey_server, project_name, context_path, use_ssl=True)
try:
    result = ssl_api.query.select_rows(schema, table)
    print(result)
except ServerContextError:
    print("Caught SSL Error")


# catch bad context path
bad_api = APIWrapper(labkey_server, project_name, "", use_ssl=False)
try:
    result = bad_api.query.select_rows(schema, table)
    print(result)
except ServerNotFoundError:
    print("Caught context path")

# catch bad folder path error
bad_api = APIWrapper(labkey_server, "bad_project_name", context_path, use_ssl=False)
try:
    result = bad_api.query.select_rows(schema, table)
    print(result)
except ServerNotFoundError:
    print("Caught bad folder name")


###################
# Test some parameters of select_rows
###################
result = api.query.select_rows(
    schema,
    table,
    max_rows=5,
    offset=10,
    include_total_count=True,
    include_details_column=True,
    include_update_column=True,
)
if result is not None:
    print("select_rows: There are " + str(len(result["rows"])) + " rows.")
    print("select_rows: There are " + str(result["rowCount"]) + " total rows.")
    print("select_rows: Response API version [" + str(result["formatVersion"]) + "].")

    column_statement = "select_rows: Included columns: "
    for column in result["columnModel"]:
        column_statement = column_statement + " " + column["header"] + ", "
    print(column_statement)

    row = result["rows"][0]
    dataIndex = result["metaData"]["id"]
    print("select_rows: The first row Key is: " + str(row[dataIndex]))
else:
    print("select_rows: Failed to load results from " + schema + "." + table)


###################
# Test get all results
###################
result = api.query.select_rows(schema, table, show_rows=Pagination.ALL, include_total_count=True)
if result is not None:
    print("select_rows: There are " + str(len(result["rows"])) + " rows.")
    print("select_rows: There are " + str(result["rowCount"]) + " total rows.")
else:
    print("select_rows: Failed to load results from " + schema + "." + table)


###################
# Test sort and select columns
###################
result = api.query.select_rows(
    schema,
    table,
    max_rows=5,
    offset=10,
    include_total_count=False,
    columns=",".join([column1, column2]),
    sort=column1 + ", -" + column2,
)  # use '-' to sort descending
if result is not None:
    print("select_rows: There are " + str(result["rowCount"]) + " rows.")
    print("select_rows: " + table)
    for row in result["rows"]:
        print("\t" + str(row[column1]) + ", " + str(row[column2]))
else:
    print("select_rows: Failed to load results from " + schema + "." + table)


###################
# Test basic filters
###################
filters = [
    QueryFilter(column1, "Group 2: HIV-1 Negative"),
    QueryFilter("Height (inches)", "50, 70", QueryFilter.Types.BETWEEN),
    QueryFilter("Country", "Germany;Uganda", QueryFilter.Types.IN),
]

result = api.query.select_rows(schema, table, filter_array=filters)
if result is not None:
    print("select_rows: There are " + str(result["rowCount"]) + " rows.")
else:
    print("select_rows: Failed to load results from " + schema + "." + table)


###################
# Test update_rows
###################
rows = result["rows"]
test_row_idx = 1
original_value = rows[test_row_idx]
column3 = "Country"
test_row = {"Key": original_value["Key"], column3: "Pangea"}

print("update_rows: original value [ " + original_value[column3] + " ]")

update_result = api.query.update_rows(schema, table, [test_row])
print("update_rows: updated value [ " + update_result["rows"][0][column3] + " ]")

update_result = api.query.update_rows(schema, table, [original_value])
print("update_rows: reset value [ " + update_result["rows"][0][column3] + " ]")


###################
# Test insert_rows & delete_rows
###################
test_row = copy.copy(original_value)

test_row["Key"] = None
test_row["Country"] = "Antarctica"

all_rows = api.query.select_rows(schema, table)
print("Insert Rows: Initials row count [ " + str(all_rows["rowCount"]) + " ]")

insert_result = api.query.insert_rows(schema, table, [test_row])
print("Insert Rows: New rowId [ " + str(insert_result["rows"][0]["Key"]) + " ]")

all_rows = api.query.select_rows(schema, table)
print("Insert Rows: after row count [ " + str(all_rows["rowCount"]) + " ]")

test_row = insert_result["rows"][0]
deleteResult = api.query.delete_rows(schema, table, [test_row])
print("Delete Rows: deleted rowId [ " + str(deleteResult["rows"][0]["Key"]) + " ]")

all_rows = api.query.select_rows(schema, table)
print("Delete Rows: after row count [ " + str(all_rows["rowCount"]) + " ]")


###################
# Test truncate_table
###################
truncate_info = api.query.truncate_table(schema, table)
print("Delete all rows in table: [ " + str(truncate_info["deletedRows"]) + " ] rows deleted")


###################
# Test execute_sql
###################
sql = "select * from lists.demographics"

# base execute_sql
sql_result = api.query.execute_sql(schema, sql)
if sql_result is not None:
    print("execute_sql: There are " + str(sql_result["rowCount"]) + " rows.")
else:
    print("execute_sql: Failed to load results from " + schema + "." + table)

# paging
sql_result = api.query.execute_sql(
    schema, sql, max_rows=5, offset=10, sort=(column1 + ", -" + column2)
)
if sql_result is not None:
    print("execute_sql: There are " + str(len(sql_result["rows"])) + " rows.")
    print("execute_sql: There are " + str(sql_result["rowCount"]) + " total rows.")
    print("execute_sql: " + table)
    for row in sql_result["rows"]:
        print("\t" + str(row[column1]) + ", " + str(row[column2]))
else:
    print("execute_sql: Failed to load results from " + schema + "." + table)

# Save query within the session
sql_result = api.query.execute_sql(schema, sql, max_rows=5, offset=10, save_in_session=True)
print("execute_sql: query saved as [ " + sql_result["queryName"] + " ]")


# set timeout
try:
    sql_result = api.query.execute_sql(schema, sql, timeout=0.001)
    print("execute_sql did not timeout")
except Timeout:
    print("Caught Timeout")


###################
# Test QC State Definitions
###################

# Create new QC state definitions
qc_states = [
    {
        "label": "needs verification",
        "description": "please look at this",
        "publicData": False,
    },
    {"label": "approved", "publicData": True},
]
result = api.query.insert_rows("core", "qcstate", qc_states)
for row in result["rows"]:
    print("Created QC state: " + row["label"])

result = api.query.select_rows("core", "qcstate")

# Update a QC state definitions
original_value = result["rows"][1]
test_row = {"RowId": original_value["RowId"], "label": "Updated Label"}
update_result = api.query.update_rows("core", "qcstate", [test_row])
print("Updated label: approved -> " + update_result["rows"][0]["label"])

# Delete all unused QC state definitions
result = api.query.select_rows("core", "qcstate")

for row in result["rows"]:
    print("Deleting QC state: " + row["Label"])
    try:
        api.query.delete_rows("core", "qcstate", [row])
    except ServerContextError as e:
        print(e.message)
