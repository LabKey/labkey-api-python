# Python API for LabKey Server
<p>
 <a href="https://pypi.python.org/pypi/labkey"><img src="https://img.shields.io/pypi/v/labkey.svg" alt="pypi version"></a>
</p>

Lets you query, insert, and update data on a [LabKey Server](https://www.labkey.com/) using Python.

## Features

The following APIs can be used against a LabKey Server instance.

Query API - [sample code](samples/query_examples.py)

- **delete_rows()** - Delete records in a table.
- **execute_sql()** - Execute SQL (LabKey SQL dialect) through the query module.
- **insert_rows()** - Insert rows into a table.
- **select_rows()** - Query and get results sets.
- **update_rows()** - Update rows in a table.
- **truncate_table()** - Delete all rows from a table.

Domain API - [sample code](samples/domain_example.py)

- **create()** - Create many types of domains (e.g. lists, datasets).
- **drop()** - Delete a domain.
- **get()** - Get a domain design.
- **infer_fields()** - Infer fields for a domain design from a file.
- **save()** - Save changes to a domain design.
- **conditional_format()** - Create a conditional format on a field.

Experiment API - [sample code](samples/experiment_example.py)

- **load_batch()** - Retrieve assay data (batch level).
- **save_batch()** - Save assay data (batch level).

Security API - [sample code](samples/security_example.py) 

- Available for administrating and configuring user accounts and permissions.

Storage API - [docs](docs/storage.md) 

- Create, update, or delete a LabKey Freezer Manager storage item.

WebDav - [docs](docs/webdav.md)

- Convenience methods for creating "webdavclient3" clients and building webdav file paths.

## Installation
To install, simply use `pip`:

```bash
$ pip install labkey
```

**Note:** For users who installed this package before it was published to PyPI (before v0.3.0) it is recommended you uninstall and reinstall the package rather than attempting to upgrade. This is due to a change in the package's versioning semantics.

## Credentials

### Set Up a netrc File

On a Mac, UNIX, or Linux system the netrc file should be named ``.netrc`` (dot netrc) and on Windows it should be named ``_netrc`` (underscore netrc). The file should be located in your home directory and the permissions on the file must be set so that you are the only user who can read it, i.e. it is unreadable to everyone else.

To create the netrc on a Windows machine, first create an environment variable called ’HOME’ that is set to your home directory (for example, C:/Users/johndoe) or any directory you want to use.

In that directory, create a text file with the prefix appropriate to your system, either an underscore or dot.

The following three lines must be included in the file. The lines must be separated by either white space (spaces, tabs, or newlines) or commas:
```
machine <remote-instance-of-labkey-server>
login <user-email>
password <user-password>
```

For example:
```
machine mymachine.labkey.org
login user@labkey.org
password mypassword
```
Note that the netrc file only deals with connections at the machine level and should not include a port or protocol designation, meaning both "mymachine.labkey.org:8888" and "https://mymachine.labkey.org" are incorrect. 

### Old credentials
As of v0.4.0 this API no longer supports using a ``.labkeycredentials.txt`` file, and now uses the .netrc files similar to the other labkey APIs. Additional .netrc [setup instructions](https://www.labkey.org/Documentation/wiki-page.view?name=netrc) can be found at the link.

## Examples

Sample code is available in the [samples](https://github.com/LabKey/labkey-api-python/tree/master/samples) directory.

The following gets data from the Users table on your local machine:

```python
from labkey.api_wrapper import APIWrapper

print("Create an APIWrapper")
labkey_server = 'localhost:8080'
project_name = 'ModuleAssayTest'  # Project folder name
contextPath = 'labkey'
schema = 'core'
table = 'Users'
api = APIWrapper(labkey_server, project_name, contextPath, use_ssl=False)

result = api.query.select_rows(schema, table)

if result is not None:
    print(result['rows'][0])
    print("select_rows: Number of rows returned: " + str(result['rowCount']))
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)
```

## Supported Versions
Python 3.7+ is fully supported.
LabKey Server v15.1 and later.

## Contributing
This package is maintained by [LabKey](http://www.labkey.com/). If you have any questions or need support, please use
the [LabKey Server developer support forum](https://www.labkey.org/home/developer/forum/project-start.view).

When contributing changes please use `Black` to format your code. To run Black follow these instructions:
1. Install black: `pip install black`
2. Run black: `black .`
3. Commit the newly formatted code.

### Testing
If you are looking to contribute please run the tests before issuing a PR. The tests can be initiated by running

```bash
$ python setup.py test
```

This runs the tests using [pytest](https://docs.pytest.org/en/latest/contents.html). If you'd like to run pytest directly you can install the testing dependencies in your virtual environment with:

```bash
$ pip install -e .[test]
```

Then, the tests can be run with
```bash
$ pytest .
```

The integration tests do not run by default. If you want to run the integration tests make sure you have a live server
running, a netrc file, and run the following command:

```bash
$ pytest . -m "integration"
```

### Maintainers
Package maintainer's can reference the [Python Package Maintenance](https://docs.google.com/document/d/13nVxwyctH4YZ6gDhcrOu9Iz6qGFPAxicE1VHiVYpw9A/) document (requires permission) for updating releases.
