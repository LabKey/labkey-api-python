# About
Python client API for LabKey Server. To get started, please see the [full documentation for this library](https://www.labkey.org/wiki/home/Documentation/page.view?name=python).

# Installation
Currently, the labkey-api-python library can only be installed via source. To install, clone this repository then run:

```bash
$ python setup.py install
```

# Credentials
In order to the use the Python client API for LabKey Server, you will need to specify your login credentials in a credential file. The package assumes that this file will be located either:

1. ``$HOME/.labkeycredentials.txt``
2. The location will be specified in the ``LABKEY_CREDENTIALS`` environment variable.

The ``labkeycredentials`` file must be in the following format. (3 separate lines):
```
machine https://hosted.labkey.com
login labkeypython@gmail.com
password python
```
where:
- machine: URL of your LabKey Server
- login: email address to be used to login to the LabKey Server
- password: password associated with the login

A sample ``labkeycredentials`` file has been shipped with the source and named ``.labkeycredentials.sample``.

# Supported Versions
Python 2.6 or 2.7 are fully supported.
LabKey Server v11.1 and later.

# Contributing
This library and the LabKey Server are maintained by the LabKey Software Foundation. If you have any questions or need support, please use the [LabKey Server support forum](https://www.labkey.org/wiki/home/page.view?name=support).