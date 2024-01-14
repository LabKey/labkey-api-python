# LabKey Domain API Overview

Create, update, or delete domain definitions as well as query domain details.

A domain is a collection of fields. Lists, Datasets, SampleTypes, DataClasses, and the Assay Batch, Run, and Result tables are backed by an LabKey internal datatype known as a Domain. Within the labkey python API, domains are objects so they have their own set of methods and attributes. These attributes can be updated so that the domain object with the updated attributes can be uploaded to a LabKey Server istance.

For more info about LabKey domains, see here, https://www.labkey.org/Documentation/wiki-page.view?name=labkeyDataStructures#domain.

### LabKey Container API Methods

To use the container API methods, you must first instantiate an APIWrapper object. See the APIWrapper docs page to learn more about how to properly do so, accounting for your LabKey Server's configuration details.

**create**

List of method parameters:
- domain_definition: A domain definition.
- container_path: labkey container path if not already set in context

**drop**

List of method parameters:
- schema_name: schema of table
- query_name: table name of domain to drop
- container_path: labkey container path if not already set in context

**get**

List of method parameters:
- schema_name: schema of table
- query_name: table name of domain to get
- container_path: labkey container path if not already set in context

**get_domain_details**

List of method parameters:
- schema_name: schema of table
- query_name: table name of domain to get
- domain_id: id of domain to get
- domain_kind: domainKind of domain to get
- container_path: labkey container path if not already set in context

**infer_fields**

List of method parameters:
- data_file: the data file from which to determine the fields shape. The data file can be a tsv, csv, or excel file.
- container_path: labkey container path if not already set in context

**save**

List of method parameters:
- schema_name: schema of domain
- query_name: query name of domain
- domain: Domain to save
- container_path: labkey container path if not already set in context
- options: associated domain options to be saved

## LabKey Domain Object, Methods, and Attributes

Domain objects are a LabKey Python API-defined class that stores information about a domain.  They are received from the domain.create, domain.get, and domain.get_domain_details methods. They can also be edited using referencing their attributes and calling their methods, which allows scripts to edit domains and reupload them to a LabKey Server instance using the domain.save method. See below for a list of their methods and attributes.

### Methods

**add_field**

This method adds the field passed into it to the Domain object that uses it. It only has one argument: field. A field is a dict object that defines a name and other field parameters such as rangeURI. Here is an 
example field: {"name": "fieldName", "rangeURI": "string"}


**to_json**

to_json returns a copy of the Domain object's data in a json format.

### Attributes

- **fields** - This attribute is an iterable object containing a set of fields and their associated properties.
- **container** - The lsid of the container where the domain is or will be defined.
- **description** - The description of the domain.
- **domain_id** - The ID value associated with the domain in its LabKey Server instance.
- **domain_uri** - The URI for the domain in its LabKey Server instance.
- **name** - The name of the domain.
- **query_name** - The query associated with the domain.
- **schema_name** - The schema of the query associated with the domain.
- **template_description** - The description of the template used to make this domain, if a template was used.

## Examples
For examples, see the /samples/domain_example.py file.

