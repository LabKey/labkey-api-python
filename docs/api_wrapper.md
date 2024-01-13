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
- This is the path to the targeted project, folder, or subfolder in a LabKey Server instance. This path will be used as the default container path for all API requests, you can override this default by passing a container_path to any API method you are using.
- Example: 'Project/Folder/Subfolder'

**context_path** 
- The default value is None. Depending on how the LabKey Server instance is implemented, it may be necessary to include a value for the context_path argument. If your LabKey Server instance has text after the base URL, that is the context path. 
- Example: If your home project has a URL such as https://labkey.org/contextpath/home/project-begin.view, then the context path is 'contextpath'.

**use_ssl**
- The default value is True. This should be set to True if your server is configured to use SSL. If you are not sure if your server uses SSL, refer to any URL for accessing your server. Servers using SSL will have a URL that begins with `https://` instead of `http://`. LabKey Sample Manager-only clients must have this argument set to True.

**verify_ssl**
- The default value is True. This argument toggles whether or not the SSL certificate is validated when attempting to connect to a server. This flag is useful when you are connecting to a development server with a self-signed SSL certificate, which would otherwise cause a failure. You should never disable this flag if you are connecting to a production server with a proper SSL certificate.

**api_key**
- The default value is None. Scripts can authenticate their LabKey API calls by using either a netrc file (details on that here, https://www.labkey.org/Documentation/wiki-page.view?name=netrc) or an API key (details about API keys and how to generate and manage them are here, https://www.labkey.org/Documentation/wiki-page.view?name=apikey). 

**disable_csrf** 
- The default value is False. In most cases, this argument must be set to False for API calls to work successfully as CSRF tokens are a fundamental security mechanism. For more info about using CSRF with your LabKey Server instance, see here, https://www.labkey.org/Documentation/wiki-page.view?name=csrfProtection.


### Using LabKey Python APIs 

The labkey-api-python library can be used to select rows, insert rows, edit containers, edit storage, modify security settings and permissions, as well as many other functions. To learn more about these different functions, see the other documentation pages in this docs folder.

### Automatic script generation

In LabKey Server, data grids by default provide the ability to generate the Python code to export the displayed grid view using the APIWrapper class and the select_rows method. This is often an easy and convenient way to create a starting point for further Python development. For more information on this topic: https://www.labkey.org/Documentation/wiki-page.view?name=exportScripts
