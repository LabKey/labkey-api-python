# APIWrapper support

Create an API session that facilitates usage of the other APIs. 

The api_wrapper class is a wrapper for all of the supported API methods in the Python Client API. This makes it easier to use the supported API methods without having to manually pass around a ServerContext object.

### Using the APIWrapper class

The APIWrapper class is imported from api_wrapper.py:

```python
from labkey.api_wrapper import APIWrapper
```

It includes the following arguments:

**Domain**
- This is the base URL for a LabKey Server instance.
- Example: 'www.labkey.org'

**Container_path**
- This is the path to the targeted project, folder, or subfolder in a LabKey Server instance. It is similar to a file path. Only absolute paths can be inputted.
- Example: 'Project/Folder/Subfolder'

**context_path** 
- The default value is None. Depending on how the LabKey Server instance is implemented, it may be necessary to include a value for the context_path argument. If your LabKey Server instance has text after the base URL, that is the context path. 
- Example: If your home project has a URL such as https://labkey.org/contextpath/home/project-begin.view, then the context path is 'contextpath'.

**
use_ssl=True

verify_ssl=True

api_key=None

disable_csrf=False



### Automatic script generation

In LabKey Server, data grids by default provide the ability to generate the Python code to export the displayed grid view using the APIWrapper class and the select_rows method. This is often an easy and convenient way to create a starting point for further Python development. For more information on this topic: https://www.labkey.org/Documentation/wiki-page.view?name=exportScripts
