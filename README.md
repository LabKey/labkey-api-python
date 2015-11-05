# About
Python client API for LabKey Server. To get started, please see the [full documentation for this library](https://www.labkey.org/wiki/home/Documentation/page.view?name=python).

# Installation
To install, simply use `pip`:

```bash
$ pip install labkey
```

# Credentials
As of v0.4.0 this API no longer supports using a ``.labkeycredentials.txt`` file, and now uses the .netrc files similar to the other labkey APIs. Additional .netrc [setup instructions](https://www.labkey.org/wiki/home/Documentation/page.view?name=netrc) can be found at the link.

## Set Up a netrc File

On a Mac, UNIX, or Linux system the netrc file should be named ``.netrc`` (dot netrc) and on Windows it should be named ``_netrc`` (underscore netrc). The file should be located in your home directory and the permissions on the file must be set so that you are the only user who can read it, i.e. it is unreadable to everyone else.

To create the netrc on a Windows machine, first create an environment variable called ’HOME’ that is set to your home directory (c:/Users/<User-Name> on Vista or Windows 7) or any directory you want to use.

In that directory, create a text file with the prefix appropriate to your system, either an underscore or dot.

The following three lines must be included in the file. The lines must be separated by either white space (spaces, tabs, or newlines) or commas:
```
machine <remote-instance-of-labkey-server>
login <user-email>
password <user-password>
```

One example would be:
```
machine mymachine.labkey.org
login user@labkey.org
password mypassword
```
Another example would be:
```
machine mymachine.labkey.org login user@labkey.org password mypassword
```

# Supported Versions
Python 2.6+ and 3.4+ are fully supported.

LabKey Server v13.3 and later.

# Contributing
This library and the LabKey Server are maintained by the LabKey Software Foundation. If you have any questions or need support, please use the [LabKey Server support forum](https://www.labkey.org/wiki/home/page.view?name=support).

