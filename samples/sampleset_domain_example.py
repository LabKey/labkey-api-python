from __future__ import unicode_literals

from labkey.utils import create_server_context
from labkey import domain

labkey_server = 'localhost:8080'
project_name = 'MySamples'  # Project folder name
context_path = 'labkey'
server_context = create_server_context(labkey_server, project_name, context_path, use_ssl=False)

###################
# Create a SampleSet domain
###################
sampleset_domain_definition = {
    'kind': 'SampleSet', 
    'domainDesign': {
        'name': 'BloodSamples',
        'description': 'Human blood samples.',
        'fields': [{
          'name': "Name", 
          'rangeURI': "string"
        },{
          'name': "volume_mL", 
          'rangeURI': "int"
        },{
          'name': "Project",
          'rangeURI': "string"
        },{
          'name': "DrawDate",
          'rangeURI': "dateTime"
        },{
          'name': "ReceivedDate",
          'rangeURI': "dateTime"
        },{
          'name': "ReceivedFrom",
          'rangeURI': "string"
        },{
          'name': "ReceivingOperator",
          'rangeURI': "string"
        },{
          'name': "TubeColor",
          'rangeURI': "string"
        },{
          'name': "TubeType",
          'rangeURI': "string"
        },{
          'name': "ProblemWithTube",
          'rangeURI': "boolean"
        },{
          'name': "Comments",
          'rangeURI': "string"
        }]
    }
}

# domain.create returns the full Domain definition
created_sampleset_domain = domain.create(server_context, sampleset_domain_definition)


###################
# Get a domain
###################
sampleset_domain = domain.get(server_context, 'samples', 'BloodSamples')

# examine different fields from the domain
print(sampleset_domain.name)
print(sampleset_domain.fields[0].name)

###################
# Save a domain
###################
sampleset_domain.add_field({
    'name': 'canTransfuse',
    'rangeURI': 'boolean'
})

# Use infer fields to define additional fields
fields_file = open('data/infer.tsv', 'rb')
inferred_fields = domain.infer_fields(server_context, fields_file)

for field in inferred_fields:
    sampleset_domain.add_field(field)

domain.save(server_context, 'samples', 'BloodSamples', sampleset_domain)

###################
# Drop a domain
###################

#drop_response = domain.drop(server_context, 'samples', 'BloodSamples')
#if 'success' in drop_response:
#    print('The SampleSet domain was deleted.')