#
# Copyright (c) 2020-2026 LabKey Corporation
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
from labkey.api_wrapper import APIWrapper

labkey_server = "localhost:8080"
container_path = "Tutorials/MySamples"  # Full project/folder container path
context_path = "labkey"
api = APIWrapper(labkey_server, container_path, context_path, use_ssl=False)

###################
# Create a SampleSet domain
###################
sampleset_domain_definition = {
    "kind": "SampleSet",
    "domainDesign": {
        "name": "BloodSamples",
        "description": "Human blood samples.",
        "fields": [
            {"name": "Name", "rangeURI": "string"},
            {"name": "volume_mL", "rangeURI": "int"},
            {"name": "Project", "rangeURI": "string"},
            {"name": "DrawDate", "rangeURI": "dateTime"},
            {"name": "ReceivedDate", "rangeURI": "dateTime"},
            {"name": "ReceivedFrom", "rangeURI": "string"},
            {"name": "ReceivingOperator", "rangeURI": "string"},
            {"name": "TubeColor", "rangeURI": "string"},
            {"name": "TubeType", "rangeURI": "string"},
            {"name": "ProblemWithTube", "rangeURI": "boolean"},
            {"name": "Comments", "rangeURI": "string"},
        ],
    },
}

# domain.create returns the full Domain definition
created_sampleset_domain = api.domain.create(sampleset_domain_definition)

###################
# Get a domain
###################
sampleset_domain = api.domain.get("samples", "BloodSamples")

# examine different fields from the domain
print(sampleset_domain.name)
print(sampleset_domain.fields[0].name)

###################
# Save a domain
###################
sampleset_domain.add_field({"name": "canTransfuse", "rangeURI": "boolean"})

# Use infer fields to define additional fields
fields_file = open("data/infer.tsv", "rb")
inferred_fields = api.domain.infer_fields(fields_file)

for field in inferred_fields:
    sampleset_domain.add_field(field)

api.domain.save("samples", "BloodSamples", sampleset_domain)

###################
# Drop a domain
###################

drop_response = api.domain.drop("samples", "BloodSamples")
if "success" in drop_response:
    print("The SampleSet domain was deleted.")
