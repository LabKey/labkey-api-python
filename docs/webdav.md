# WebDav Support

Our Python API includes some convenience methods for creating "webdavclient3" clients, and building webdav file paths.

### Creating a WebDav client
First, make sure you have the [webdavclient3](https://github.com/ezhov-evgeny/webdav-client-python-3) library installed:

```bash
$ pip install webdavclient3
```

Then you can use your `APIWrapper` to create a client:

```python
from labkey.api_wrapper import APIWrapper

domain = "localhost:8080"
container = "MyContainer"
api = APIWrapper(domain, container)
webdav_client = api.server_context.webdav_client()
```

The `webdav_client` method has a single optional argument, `webdav_options`, a dict that you can use to pass any options
that you would pass to the [webdavclient3](https://github.com/ezhov-evgeny/webdav-client-python-3#webdav-api) library.
If you are using API Key authentication with your APIWrapper we will automatically configure the WebDav Client to use
API Key authentication with your API Key. If you are using a `.netrc` file for authentication it should automatically
detect your `.netrc` file and authenticate using those credentials. 


### The webdav_path utility method
If you are using the `webdavclient3` library you'll still need to know the appropriate WebDav path in order to access
your files. We provide a utility method, `webdav_path` to make it easier to construct LabKey WebDav paths. The method
takes to keyword arguments, `container_path`, and `file_name`.

```python
from labkey.api_wrapper import APIWrapper

domain = "localhost:8080"
container = "MyContainer"
api = APIWrapper(domain, container)
webdav_client = api.server_context.webdav_client()

# Constructs a webdav path to "MyContainer"
path = api.server_context.webdav_path()
print(webdav_client.info(path))
# Constructs a webdav path to the "data.txt" file in "MyContainer"
path = api.server_context.webdav_path(file_name='data.txt')
print(webdav_client.info(path))
# Constructs a webdav path to the "data.txt" file in "other_container"
path = api.server_context.webdav_path(container_path="other_container", file_name="data.txt")
print(webdav_client.info(path))
```
