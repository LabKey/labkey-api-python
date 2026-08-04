# LabKey Query API Support

The Query API reads and writes data in any LabKey schema. Every method targets a table or query by its **schema
name** and **query name** — the same pair shown in the server UI under Admin → Go To Module → Query, and in the
URL of any data grid (e.g. `.../query-executeQuery.view?schemaName=lists&query.queryName=Demographics`).

The API is modeled after the LabKey JavaScript client API of the same name, so the method names and payloads
correspond closely to their JavaScript counterparts.

### Additional details from LabKey Documentation:
- [LabKey Client APIs](https://www.labkey.org/Documentation/wiki-page.view?name=viewAPIs)
- [Container Filters](https://www.labkey.org/download/clientapi_docs/javascript-api/symbols/LABKEY.Query.html#.containerFilter)

## Interfaces

The classes below are imported from `labkey.query`:

```python
from labkey.query import AuditBehavior, Pagination, QueryFilter
```

### `QueryFilter`

Represents a single filter clause. Pass a list of them as the `filter_array` argument to `select_rows`.

```python
QueryFilter(column, value, filter_type=QueryFilter.Types.EQUAL)
```

| Argument      | Type  | Description                                                                     |
|---------------|-------|---------------------------------------------------------------------------------|
| `column`      | `str` | Name of the column to filter on.                                                |
| `value`       | `str` | The value to compare against. Ignored by the "no data value" types below.       |
| `filter_type` | `str` | One of `QueryFilter.Types`. Defaults to `EQUAL`.                                |

Multiple filters may target the same column; each is applied.

`QueryFilter.Types` enumerates the available operators:

| Category                | Types                                                                                                                                                                                        |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Equality                | `EQUAL`, `NEQ` / `NOT_EQUAL`, `NEQ_OR_NULL` / `NOT_EQUAL_OR_MISSING`, `DATE_EQUAL`, `DATE_NOT_EQUAL`                                                                                          |
| Comparison              | `GT` / `GREATER_THAN`, `GTE` / `GREATER_THAN_OR_EQUAL`, `LT` / `LESS_THAN`, `LTE` / `LESS_THAN_OR_EQUAL`, and the `DATE_` prefixed equivalents                                                |
| Ranges and sets         | `BETWEEN`, `NOT_BETWEEN`, `IN` / `EQUALS_ONE_OF`, `NOT_IN` / `EQUALS_NONE_OF`, `MEMBER_OF`                                                                                                    |
| Strings                 | `STARTS_WITH`, `DOES_NOT_START_WITH`, `CONTAINS`, `DOES_NOT_CONTAIN`, `CONTAINS_ONE_OF`, `CONTAINS_NONE_OF`                                                                                   |
| Arrays                  | `ARRAY_CONTAINS_ALL`, `ARRAY_CONTAINS_ANY`, `ARRAY_CONTAINS_NONE`, `ARRAY_CONTAINS_EXACT`, `ARRAY_CONTAINS_NOT_EXACT`, `ARRAY_ISEMPTY`, `ARRAY_ISNOTEMPTY`                                    |
| No data value           | `HAS_ANY_VALUE`, `IS_BLANK`, `IS_NOT_BLANK`, `HAS_MISSING_VALUE`, `DOES_NOT_HAVE_MISSING_VALUE`                                                                                               |
| Search, ontology, lineage | `Q` (table-wide search), `ONTOLOGY_IN_SUBTREE`, `ONTOLOGY_NOT_IN_SUBTREE`, `EXP_CHILD_OF`, `EXP_PARENT_OF`, `EXP_LINEAGE_OF`                                                                |

Multi-value types are not consistent in how they delimit values — this is a historical artifact of the underlying
API. `BETWEEN` and `NOT_BETWEEN` take a comma separated pair (`"50, 70"`); `IN` and `NOT_IN` take a semicolon
separated list (`"Germany;Uganda"`).

### `Pagination`

Paging styles for the `show_rows` argument of `select_rows`: `PAGINATED`, `SELECTED`, `UNSELECTED`, `ALL`, `NONE`.

### `AuditBehavior`

Overrides the audit detail level of a write operation: `DETAILED`, `SUMMARY`, `NONE`. `DETAILED` records the
values before and after the change, `SUMMARY` records only that a change occurred. When omitted, the table's
configured behavior applies.

### `Command`

A `TypedDict` describing one operation in a `save_rows` request. Keys use Python style names and are converted to
the server's JSON names for you.

| Key                  | Type                                 | Required | Description                                                       |
|----------------------|--------------------------------------|----------|-------------------------------------------------------------------|
| `command`            | `"insert"` / `"update"` / `"delete"` | Yes      | The operation to perform.                                         |
| `schema_name`        | `str`                                | Yes      | Schema of the target table.                                       |
| `query_name`         | `str`                                | Yes      | Target table name.                                                |
| `rows`               | `List[dict]`                         | Yes      | The rows to insert, update, or delete.                            |
| `container_path`     | `str`                                | No       | Overrides the container for this command only.                    |
| `audit_behavior`     | `AuditBehavior`                      | No       | Audit detail level for this command.                              |
| `audit_user_comment` | `str`                                | No       | Comment attached to detailed audit records.                       |
| `extra_context`      | `dict`                               | No       | Passed to the transformation/validation script environment.       |
| `skip_reselect_rows` | `bool`                               | No       | Skip returning the full detail of the affected rows.              |

## Methods

All methods are available on the `query` member of an `APIWrapper` instance.

| Method                                                          | Description                                                                     |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------|
| `select_rows(schema_name, query_name, ...)`                     | Query a table or query and return the result set.                               |
| `execute_sql(schema_name, sql, ...)`                            | Execute LabKey SQL against a schema.                                            |
| `insert_rows(schema_name, query_name, rows, ...)`               | Insert rows into a table.                                                       |
| `update_rows(schema_name, query_name, rows, ...)`               | Update existing rows. Each row must carry its primary key.                      |
| `delete_rows(schema_name, query_name, rows, ...)`               | Delete rows. Each row need only carry its primary key.                          |
| `move_rows(target_container_path, schema_name, query_name, rows, ...)` | Move rows to another container.                                           |
| `truncate_table(schema_name, query_name, ...)`                  | Delete every row in a table.                                                    |
| `import_rows(schema_name, query_name, data_file, ...)`          | Bulk insert or merge rows from a file.                                          |
| `save_rows(commands, ...)`                                      | Perform inserts, updates, and deletes across several tables in one request.      |
| `get_queries(schema_name, ...)`                                 | List the queries available in a schema.                                         |

### Common arguments

| Argument             | Default    | Description                                                                                                 |
|----------------------|------------|-------------------------------------------------------------------------------------------------------------|
| `container_path`     | `None`     | Overrides the container path configured on the `APIWrapper` for this request.                                |
| `transacted`         | `True`     | Whether the writes are applied in a single transaction, so that they all succeed or all fail.                |
| `audit_behavior`     | `None`     | See [`AuditBehavior`](#auditbehavior).                                                                       |
| `audit_user_comment` | `None`     | Comment attached to certain detailed audit log records.                                                      |
| `timeout`            | `300`      | Request timeout in seconds. Exceeding it raises `requests.exceptions.Timeout`.                                |

`container_path`, `transacted`, `audit_behavior`, and `audit_user_comment` apply to the write methods
(`insert_rows`, `update_rows`, `delete_rows`, `move_rows`); read methods accept `container_path` and `timeout`.

### Notable per-method arguments

`select_rows`

| Argument                 | Default | Description                                                                                            |
|--------------------------|---------|--------------------------------------------------------------------------------------------------------|
| `view_name`              | `None`  | Name of an existing custom view to apply.                                                              |
| `filter_array`           | `None`  | List of [`QueryFilter`](#queryfilter) objects.                                                         |
| `columns`                | `None`  | Comma separated list of columns to retrieve. Lookups may be traversed with `/`, e.g. `"Sample/Name"`.   |
| `max_rows`               | `-1`    | Maximum rows to return. `-1` means unlimited.                                                          |
| `offset`                 | `None`  | Number of rows to skip.                                                                                |
| `sort`                   | `None`  | Comma separated column list. Prefix a column with `-` to sort descending.                              |
| `show_rows`              | `None`  | A [`Pagination`](#pagination) value.                                                                   |
| `include_total_count`    | `None`  | Include the total row count in the response, independent of paging.                                     |
| `include_details_column` | `None`  | Include a Details link column in the results.                                                          |
| `include_update_column`  | `None`  | Include an Update link column in the results.                                                          |
| `container_filter`       | `None`  | Broadens the query beyond the target container. See the link at the top of this page.                   |
| `parameters`             | `None`  | Values for a parameterized query, as a dict.                                                            |
| `ignore_filter`          | `None`  | When `True`, filters saved on the chosen view are ignored.                                              |
| `required_version`       | `None`  | Response format version.                                                                               |

`execute_sql` accepts `container_filter`, `max_rows`, `offset`, `sort`, `parameters`, `required_version`, and:

| Argument          | Default | Description                                                                                                       |
|-------------------|---------|-------------------------------------------------------------------------------------------------------------------|
| `save_in_session` | `None`  | Save the query in the session. The response's `queryName` can then be passed to `select_rows` as `query_name`.      |
| `waf_encode_sql`  | `True`  | Encode the SQL so that web application firewalls do not reject the request. Rarely needs to change.                 |

`import_rows`

| Argument                        | Default    | Description                                                                                                   |
|---------------------------------|------------|---------------------------------------------------------------------------------------------------------------|
| `data_file`                     | required   | An open file handle. Its column headers must match the LabKey column names.                                     |
| `insert_option`                 | `"INSERT"` | `"INSERT"` creates a new row for every row in the file; `"MERGE"` updates rows that already exist and inserts the rest. When merging you only need to supply the columns you want to change. |
| `audit_behavior`                | `None`     | `"SUMMARY"` or `"DETAILED"`. Defaults to the setting on the LabKey query.                                       |
| `import_lookup_by_alternate_key`| `False`    | Resolve lookup targets by value rather than by primary key. Only works for lookups configured with unique column information. |

`save_rows`

| Argument        | Default | Description                                                                                                          |
|-----------------|---------|----------------------------------------------------------------------------------------------------------------------|
| `commands`      | required| A list of [`Command`](#command) dicts.                                                                               |
| `api_version`   | `None`  | When `13.2` or higher, a request that fails validation is returned as a successful response — check `errorCount` and `committed` — instead of raising. |
| `transacted`    | `None`  | Whether all commands are applied in one transaction. Defaults to `True` on the server.                                |
| `validate_only` | `None`  | Run every command but commit nothing. Useful for incremental validation of a UI form.                                  |
| `extra_context` | `None`  | Passed to the transformation/validation script environment for all commands.                                          |

`get_queries` accepts `include_columns`, `include_system_queries`, `include_title`, `include_user_queries`,
`include_view_data_url` (all default `True`), and `query_detail_columns` (default `False`, and only meaningful when
`include_columns` is `True`).

## Responses

All methods return the decoded JSON response as a dict.

`select_rows` and `execute_sql` return:

| Key           | Description                                                                        |
|---------------|------------------------------------------------------------------------------------|
| `rows`        | A list of dicts, one per row, keyed by column name.                                |
| `rowCount`    | Number of rows. Reflects the total row count when `include_total_count` is `True`.  |
| `columnModel` | Metadata for each returned column, including its `header`.                          |
| `metaData`    | Result set metadata, including `id` — the name of the primary key column.           |
| `schemaName`  | The queried schema. `execute_sql` reports `queryName` as `"sql"`.                    |
| `queryName`   | The queried table, or the session query name when `save_in_session` is used.         |

`insert_rows`, `update_rows`, `delete_rows`, and `move_rows` return `rowsAffected` and a `rows` list holding the
affected rows as they exist after the operation. `truncate_table` returns `deletedRows`. `import_rows` returns
`success` and `rowCount`, or `success: False` with `errorCount` and `errors` — it reports validation failures in the
response rather than raising. `save_rows` returns `committed`, `errorCount`, and `result`, a list parallel to
`commands` where each entry has its own `rowsAffected` and `rows`. `get_queries` returns `schemaName` and `queries`.

Note that keys in write responses are lower cased by the server, so a `RowId` column is read back as `rowid`.

## Exceptions

Errors are raised as subclasses of `labkey.exceptions.RequestError`, which extends
`requests.exceptions.RequestException`. All of them expose a `message` attribute containing the HTTP status code
and the server's error text.

| Exception                    | Raised when                                                                            |
|------------------------------|----------------------------------------------------------------------------------------|
| `RequestError`               | Base class. Catch this to handle any server error.                                     |
| `QueryNotFoundError`         | The schema or query does not exist.                                                    |
| `RequestAuthorizationError`  | The user is not authorized for the request.                                            |
| `ServerNotFoundError`        | The server resource was not found — usually a bad context path or container path.       |
| `UnexpectedRedirectError`    | The server redirected the request, e.g. from `http` to `https`.                          |
| `ServerContextError`         | The request could not be completed — connection, SSL, or URL parsing failure — or the server rejected the operation with an error message. |

### Examples

Every example below uses an `APIWrapper` instance to make its requests. See [api_wrapper.md](api_wrapper.md) for the
full set of `APIWrapper` arguments, including how to configure the container path, context path, SSL, and
authentication.

#### Select rows

```python
from labkey.api_wrapper import APIWrapper
from labkey.query import Pagination

labkey_server = "www.example.com"
container_path = "Tutorials/HIV Study"  # Full project/folder container path
context_path = "labkey"
api = APIWrapper(labkey_server, container_path, context_path)

schema = "lists"
table = "Demographics"

###################
# Basic select_rows
###################
result = api.query.select_rows(schema, table)

if result is not None:
    print(result["rows"][0])
    print("select_rows: There are " + str(result["rowCount"]) + " rows.")
else:
    print("select_rows: Failed to load results from " + schema + "." + table)

###################
# Page the results and read the response metadata
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
print("select_rows: There are " + str(len(result["rows"])) + " rows.")
print("select_rows: There are " + str(result["rowCount"]) + " total rows.")

columns = [column["header"] for column in result["columnModel"]]
print("select_rows: Included columns: " + ", ".join(columns))

key_column = result["metaData"]["id"]
print("select_rows: The first row key is: " + str(result["rows"][0][key_column]))

###################
# Retrieve every row, regardless of the default page size
###################
result = api.query.select_rows(schema, table, show_rows=Pagination.ALL, include_total_count=True)

###################
# Select specific columns, sorted ascending by one and descending by another
###################
result = api.query.select_rows(
    schema,
    table,
    columns="Group Assignment, Participant ID",
    sort="Group Assignment, -Participant ID",  # use '-' to sort descending
)
for row in result["rows"]:
    print("\t" + str(row["Group Assignment"]) + ", " + str(row["Participant ID"]))
```

#### Filter rows

```python
from labkey.api_wrapper import APIWrapper
from labkey.query import QueryFilter

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

filters = [
    QueryFilter("Group Assignment", "Group 2: HIV-1 Negative"),
    QueryFilter("Height (inches)", "50, 70", QueryFilter.Types.BETWEEN),
    QueryFilter("Country", "Germany;Uganda", QueryFilter.Types.IN),
]

result = api.query.select_rows("lists", "Demographics", filter_array=filters)
print("select_rows: There are " + str(result["rowCount"]) + " rows.")
```

#### Execute LabKey SQL

```python
from labkey.api_wrapper import APIWrapper

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

schema = "lists"
sql = "SELECT * FROM lists.Demographics"

result = api.query.execute_sql(schema, sql)
print("execute_sql: There are " + str(result["rowCount"]) + " rows.")

###################
# Paging and sorting are applied the same way as in select_rows
###################
result = api.query.execute_sql(schema, sql, max_rows=5, offset=10, sort="Country")

###################
# Save the results in the session, then query them by name
###################
result = api.query.execute_sql(schema, sql, save_in_session=True)
session_query = result["queryName"]
print("execute_sql: query saved as [ " + session_query + " ]")

result = api.query.select_rows(schema, session_query)
```

#### Insert, update, and delete rows

```python
from labkey.api_wrapper import APIWrapper
from labkey.query import AuditBehavior

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

schema = "lists"
table = "Demographics"

###################
# Insert. The response holds the inserted rows, including their new keys.
###################
result = api.query.insert_rows(schema, table, [{"Country": "Antarctica"}])
new_key = result["rows"][0]["Key"]
print("insert_rows: new rowId [ " + str(new_key) + " ]")

###################
# Update. Supply the primary key plus only the columns being changed.
###################
result = api.query.update_rows(
    schema,
    table,
    [{"Key": new_key, "Country": "Pangea"}],
    audit_behavior=AuditBehavior.DETAILED,
    audit_user_comment="Corrected the country of origin.",
)
print("update_rows: updated value [ " + result["rows"][0]["Country"] + " ]")

###################
# Delete. The primary key is all that is required.
###################
result = api.query.delete_rows(schema, table, [{"Key": new_key}])
print("delete_rows: deleted rowId [ " + str(result["rows"][0]["Key"]) + " ]")

###################
# Delete every row in the table
###################
result = api.query.truncate_table(schema, table)
print("truncate_table: [ " + str(result["deletedRows"]) + " ] rows deleted")
```

#### Save changes to several tables in one request

`save_rows` applies any mix of inserts, updates, and deletes in a single transaction, across as many tables as
needed. Values in the `MaterialInputs/<SampleType>` and `DataInputs/<DataClass>` form register lineage on the
inserted rows.

```python
from labkey.api_wrapper import APIWrapper

api = APIWrapper("www.example.com", "Biologics")

commands = [
    {
        "command": "insert",
        "schema_name": "samples",
        "query_name": "Blood",
        "rows": [
            {"name": "BL-3", "MaterialInputs/Tissues": "T-1"},
            {"name": "BL-4", "MaterialInputs/Blood": "BL-2"},
        ],
    },
    {
        "command": "update",
        "schema_name": "samples",
        "query_name": "Tissues",
        "rows": [{"rowId": 1234, "ReceivedDate": "2025-07-07 12:34:56"}],
    },
    {
        "command": "delete",
        "schema_name": "samples",
        "query_name": "Blood",
        "rows": [{"rowId": 5678}],
    },
]

result = api.query.save_rows(commands=commands)

print("save_rows: committed [ " + str(result["committed"]) + " ]")
for index, command_result in enumerate(result["result"]):
    print("command " + str(index) + ": " + str(command_result["rowsAffected"]) + " rows affected")
```

By default a command that fails validation raises a `ServerContextError`. Pass `api_version=13.2` to receive the
failure as a normal response instead, which is useful when you want to report every error rather than just the
first one.

```python
result = api.query.save_rows(api_version=13.2, commands=commands)

if not result["committed"]:
    print("save_rows: " + str(result["errorCount"]) + " error(s), nothing was committed")
    for command_result in result["result"]:
        if "errors" in command_result:
            print(command_result["errors"]["exception"])
```

#### Import rows from a file

`import_rows` is the efficient way to load a large number of rows. Unlike the other write methods it reports
validation problems in its response rather than raising.

```python
from labkey.api_wrapper import APIWrapper

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

with open("demographics.csv", "r") as data_file:
    result = api.query.import_rows("lists", "Demographics", data_file=data_file)

if result["success"]:
    print("import_rows: imported " + str(result["rowCount"]) + " rows")
else:
    print("import_rows: " + str(result["errorCount"]) + " error(s)")
    for error in result["errors"]:
        print(error["exception"])
```

To update existing rows from the same file, import with the `"MERGE"` option. If the file identifies lookup values
by name rather than by row id — a `parent` column holding `parent_one` instead of `1` — set
`import_lookup_by_alternate_key` so the server resolves them.

```python
with open("child_data.csv", "r") as data_file:
    result = api.query.import_rows(
        "lists",
        "child_list",
        data_file=data_file,
        insert_option="MERGE",
        import_lookup_by_alternate_key=True,
    )
```

#### Move rows to another container

`move_rows` takes the destination container as its first argument. The source container is the one configured on
the `APIWrapper`, or whatever is passed as `container_path`.

```python
from labkey.api_wrapper import APIWrapper

api = APIWrapper("www.example.com", "Biologics")

result = api.query.move_rows(
    "Biologics/Archive",
    "samples",
    "Blood",
    [{"rowId": 1234}, {"rowId": 5678}],
    audit_user_comment="Archiving samples from the completed study.",
)
print("move_rows: moved " + str(result["rowsAffected"]) + " rows")
```

#### List the queries in a schema

```python
from labkey.api_wrapper import APIWrapper

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

result = api.query.get_queries("core")
for query in result["queries"]:
    print(query["name"] + " — " + query["title"])

###################
# Limit the results to queries defined by a module
###################
result = api.query.get_queries("core", include_system_queries=False, include_user_queries=False)
```

#### Handle errors

```python
from labkey.api_wrapper import APIWrapper
from labkey.exceptions import QueryNotFoundError, RequestError, ServerContextError
from requests.exceptions import Timeout

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

# A missing schema or query
try:
    api.query.select_rows("lists", "NoSuchTable")
except QueryNotFoundError as e:
    print("Query not found: " + e.message)

# An operation the server rejects
try:
    api.query.delete_rows("core", "datastates", [{"rowid": 1}])
except ServerContextError as e:
    print("Server rejected the request: " + e.message)

# Any server error
try:
    api.query.select_rows("badSchema", "Demographics")
except RequestError as e:
    print("Request failed: " + e.message)

# A request that takes too long
try:
    api.query.execute_sql("lists", "SELECT * FROM lists.Demographics", timeout=0.001)
except Timeout:
    print("Request timed out")
```

#### In depth: managing QC states

This example is longer than the others and combines several of the methods above. It walks through the full life
cycle of a QC state definition in a study folder: creating states, renaming one, assigning one to a dataset row,
and cleaning up. Along the way it shows how the server's constraints surface through the API.

QC state definitions live in `core.DataStates`. The related `core.QCState` table is a read-only view over the same
rows that excludes LIMS sample statuses (rows with a non-null `StateType`), so writes must target
`core.DataStates`.

```python
from labkey.api_wrapper import APIWrapper
from labkey.exceptions import ServerContextError
from labkey.query import AuditBehavior, QueryFilter

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

###################
# Create two QC state definitions. publicData controls whether data in this
# state is visible to users who lack permission to view unapproved data.
###################
qc_states = [
    {
        "label": "needs verification",
        "description": "that can not be right",
        "publicData": False,
    },
    {"label": "approved", "publicData": True},
]

result = api.query.insert_rows("core", "DataStates", qc_states)
print("Created " + str(result["rowsAffected"]) + " QC states")

# Note the lower cased keys in write responses
needs_verification_id = result["rows"][0]["rowid"]
approved_id = result["rows"][1]["rowid"]

###################
# Labels are unique per container, so re-creating one is an error
###################
try:
    api.query.insert_rows("core", "DataStates", [{"label": "approved", "publicData": True}])
except ServerContextError as e:
    print("Duplicate label rejected: " + e.message)

###################
# Update a definition. Only the primary key and the changed columns are needed.
###################
result = api.query.update_rows(
    "core",
    "DataStates",
    [{"rowid": needs_verification_id, "description": "for sure that is not right"}],
    audit_behavior=AuditBehavior.DETAILED,
    audit_user_comment="Clarified the description for reviewers.",
)
print("Updated description: " + result["rows"][0]["description"])

###################
# Assign the state to a dataset row. QCState is a lookup to core.DataStates,
# so it takes the state's rowId.
###################
result = api.query.insert_rows(
    "study",
    "Lab Results",
    [
        {
            "ParticipantId": "2",
            "SequenceNum": "345",
            "Value": 4,
            "QCState": needs_verification_id,
        }
    ],
)
dataset_row_lsid = result["rows"][0]["lsid"]

###################
# List the states that are defined, and which are public
###################
result = api.query.select_rows(
    "core",
    "DataStates",
    columns="RowId, Label, Description, PublicData",
    filter_array=[QueryFilter("StateType", "", QueryFilter.Types.IS_BLANK)],
    sort="Label",
)
for row in result["rows"]:
    print(row["Label"] + " (public: " + str(row["PublicData"]) + ")")

###################
# A state that is in use cannot be deleted
###################
try:
    api.query.delete_rows("core", "DataStates", [{"rowid": needs_verification_id}])
except ServerContextError as e:
    # 400: State 'needs verification' cannot be deleted as it is currently in use.
    print("Delete blocked: " + e.message)

###################
# Stop using the state, then clean up both definitions. Dataset rows are keyed
# by LSID rather than by an integer row id.
###################
api.query.delete_rows("study", "Lab Results", [{"lsid": dataset_row_lsid}])
api.query.delete_rows(
    "core",
    "DataStates",
    [{"rowid": needs_verification_id}, {"rowid": approved_id}],
)
```

The same sequence can be expressed as a single `save_rows` request when the operations do not depend on ids
returned by earlier steps — for example deleting the dataset row and its QC state together, so that neither is
applied if the other fails.

```python
result = api.query.save_rows(
    commands=[
        {
            "command": "delete",
            "schema_name": "study",
            "query_name": "Lab Results",
            "rows": [{"lsid": dataset_row_lsid}],
        },
        {
            "command": "delete",
            "schema_name": "core",
            "query_name": "DataStates",
            "rows": [{"rowid": needs_verification_id}],
        },
    ]
)
print("save_rows: committed [ " + str(result["committed"]) + " ]")
```
