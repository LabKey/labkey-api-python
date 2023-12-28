# LabKey Query API Overview

Insert data into LabKey tables, update data in them, select data in them, or delete rows from them.

In LabKey Server, data is stored within tables called data grids. This API lets users interact with these data grids with scripts instead of using the browser GUI.

For more info about LabKey data grids and interacting with them see here, https://www.labkey.org/Documentation/wiki-page.view?name=datasetViews.

### LabKey Query API Methods

To use the query API methods, you must first instantiate an APIWrapper object. See the APIWrapper docs page to learn more about how to properly do so, accounting for your LabKey Server's configuration details.

**delete_rows**

List of method parameters:
- schema_name: schema of table
- query_name: table name to delete from
- rows: Set of rows to delete
- container_path: labkey container path if not already set in context
- timeout: timeout of request in seconds (defaults to 30s)

**truncate_table**

List of method parameters:
- schema_name: schema of table
- query_name: table name to delete from
- container_path: labkey container path if not already set in context
- timeout: timeout of request in seconds (defaults to 30s)

**execute_sql**

List of method parameters:
- schema_name: schema of table
- sql: String of labkey sql to execute
- container_path: labkey container path if not already set in context
- max_rows: max number of rows to return
- sort: comma separated list of column names to sort by
- offset: number of rows to offset results by
- container_filter: enumeration of the various container filters available. See: https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Query.html#.containerFilter
- save_in_session: save query result as a named view to the session
- parameters: parameter values to pass through to a parameterized query
- required_version: Api version of response
- timeout: timeout of request in seconds (defaults to 30s)
- waf_encode_sql: WAF encode sql in request (defaults to True)

**insert_rows**

List of method parameters:
- schema_name: schema of table
- query_name: table name to insert into
- rows: set of rows to insert
- container_path: labkey container path if not already set in context
- timeout: timeout of request in seconds (defaults to 30s)

**select_rows**

List of method parameters:
- schema_name: schema of table
- query_name: table name to select from
- view_name: pre-existing named view
- filter_array: set of filter objects to apply
- container_path: folder path if not already part of server_context
- columns: set of columns to retrieve
- max_rows: max number of rows to retrieve, defaults to -1 (unlimited)
- sort: comma separated list of column names to sort by, prefix a column with '-' to sort descending
- offset: number of rows to offset results by
- container_filter: enumeration of the various container filters available. See: https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Query.html#.containerFilter
- parameters: Set of parameters to pass along to a parameterized query. See here for more info, https://www.labkey.org/Documentation/wiki-page.view?name=paramsql
- show_rows: An enumeration of various paging styles
- include_total_count: Boolean value that indicates whether to include a total count value in response
- include_details_column: Boolean value that indicates whether to include a Details link column in results
- include_update_column: Boolean value that indicates whether to include an Update link column in results
- selection_key:
- required_version: decimal value that indicates the response version of the api
- timeout: Request timeout in seconds (defaults to 30s)
- ignore_filter: Boolean, if true, the command will ignore any filter that may be part of the chosen view.
  
**update_rows**

List of method parameters:
- schema_name: schema of table
- query_name: table name to update
- rows: Set of rows to update
- container_path: labkey container path if not already set in context
- timeout: timeout of request in seconds (defaults to 30s)
