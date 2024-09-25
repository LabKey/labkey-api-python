#
# Copyright (c) 2024 LabKey Corporation
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
container_path = "Tutorials/HIV Study"  # Full project/folder container path
api = APIWrapper(labkey_server, container_path, use_ssl=False)

###################
# Create an assay protocol
###################

# Define run domain fields
run_fields = [
    {"name": "runRunRun"}
]

# Define result domain fields
result_fields = [
    {"name": "resultResultResult"},
    {
        "conceptURI": "http://www.labkey.org/exp/xml#sample",
        "lookupQuery": "Materials",
        "lookupSchema": "exp",
        "name": "sampleLookupField",
        "rangeURI": "http://www.w3.org/2001/XMLSchema#int"
    }
]

# Specify the assay protocol definition
assay_protocol_definition = {
    "editableResults": True,
    "editableRuns": True,
    "domains": [
        {
            "domainKindName": "Assay",
            "domainURI": "urn:lsid:${LSIDAuthority}:AssayDomain-Batch.Folder-${Container.RowId}:${GpatAssayDBSeq}",
            "name": "Batch Fields"
        },
        {
            "domainKindName": "Assay",
            "domainURI": "urn:lsid:${LSIDAuthority}:AssayDomain-Run.Folder-${Container.RowId}:${GpatAssayDBSeq}",
            "name": "Run Fields",
            "fields": run_fields
        },
        {
            "domainKindName": "Assay",
            "domainURI": "urn:lsid:${LSIDAuthority}:AssayDomain-Data.Folder-${Container.RowId}:${GpatAssayDBSeq}",
            "name": "Data Fields",
            "fields": result_fields
        }
    ],
    "name": "Assay Protocol Created Using Python",
    "providerName": "General"
}

url = api.server_context.build_url("assay", "saveProtocol.api", container_path=container_path)
assay_protocol = api.server_context.make_request(url, json=assay_protocol_definition)

# Display a success message
print(assay_protocol["message"])
