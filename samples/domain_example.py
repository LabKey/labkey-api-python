#
# Copyright (c) 2018 LabKey Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import unicode_literals

from labkey.utils import create_server_context
from labkey import domain

labkey_server = 'localhost:8080'
project_name = 'Study'  # Project folder name
context_path = 'labkey'
server_context = create_server_context(labkey_server, project_name, context_path, use_ssl=False)

###################
# Create a list domain
###################
list_domain_definition = {
    'kind': 'IntList',  # or 'VarList'
    'domainDesign': {
        'name': 'BloodTypes',
        'description': 'All known human blood types',
        'fields': [{
            'name': 'rowId',
            'rangeURI': 'int'
        }, {
            'name': 'type',
            'rangeURI': 'string'
        }]
    },
    # 'options' allows for passing properties specific to a domain type (e.g. list, dataset, etc)
    'options': {
        'keyName': 'rowId',
        'keyType': 'AutoIncrementInteger'
    }
}

# domain.create returns the full Domain definition
created_list_domain = domain.create(server_context, list_domain_definition)

###################
# Create a study dataset domain
###################
dataset_domain_definition = {
    'kind': 'StudyDatasetDate',  # or 'StudyDatasetVisit'
    'domainDesign': {
        'name': 'Blood Levels',
        'fields': [{
            'name': 'vitd',
            'label': 'Vitamin D (ng/mL)',
            'rangeURI': 'double'
        }, {
            'name': 'type',
            'rangeURI': 'int',
            'lookupSchema': 'lists',
            'lookupQuery': 'BloodTypes',
            'setMeasure': True
        }]
    }
}

dataset_domain = domain.create(server_context, dataset_domain_definition)

###################
# Get a domain
###################
list_domain = domain.get(server_context, 'lists', 'BloodTypes')

# examine different from the domain
print(list_domain.name)
print(list_domain.fields[0].name)

###################
# Save a domain
###################
list_domain.add_field({
    'name': 'canTransfuse',
    'rangeURI': 'boolean'
})

# Use infer fields to define additional fields
fields_file = open('data/infer.tsv', 'rb')
inferred_fields = domain.infer_fields(server_context, fields_file)

for field in inferred_fields:
    list_domain.add_field(field)

domain.save(server_context, 'lists', 'BloodTypes', list_domain)

###################
# Drop a domain
###################
drop_response = domain.drop(server_context, 'study', 'Blood Levels')
if 'success' in drop_response:
    print('The dataset domain was deleted.')

drop_response = domain.drop(server_context, 'lists', 'BloodTypes')
if 'success' in drop_response:
    print('The list domain was deleted.')
