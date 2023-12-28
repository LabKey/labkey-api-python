# LabKey Domain API Overview

Create, update, or delete domain definitions as well as query domain details.

A domain is a collection of fields. Lists, Datasets, SampleTypes, DataClasses, and the Assay Batch, Run, and Result tables are backed by an LabKey internal datatype known as a Domain.

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
- data_file: the data file from which to determine the fields shape
- container_path: labkey container path if not already set in context

**save**

List of method parameters:
- schema_name: schema of domain
- query_name: query name of domain
- domain: Domain to save
- container_path: labkey container path if not already set in context
- options: associated domain options to be saved
