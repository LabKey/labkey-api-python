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
from labkey.utils import create_server_context
from labkey.experiment import Batch, Run, save_batch

labkey_server = "localhost:8080"
project_name = "assays"  # Project folder name
context_path = "labkey"
server_context = create_server_context(labkey_server, project_name, context_path, use_ssl=False)

assay_id = 310  # provide one from your server

###################
# Save an Assay batch
###################

# Generate the Run object(s)
run_test = Run()
run_test.name = "python upload"
run_test.data_rows = [
    {
        # ColumnName: Value
        "ParticipantId": "1234",
        "VisitId": 111,
        "WellLocation": "A1",
    },
    {"ParticipantId": "5678", "VisitId": 222, "WellLocation": "B11"},
    {"ParticipantId": "9123", "VisitId": 333, "WellLocation": "F12"},
]

# Assays that are configured for plate support have a required run property for the plate template, this is the plate
# template lsid
run_test.properties[
    "PlateTemplate"
] = "urn:lsid:labkey.com:PlateTemplate.Folder-6:d8bbec7d-34cd-1038-bd67-b3bd777822f8"

# The assay plate metadata is a specially formatted JSON object to map properties to the well groups
run_test.plate_metadata = {
    "control": {"positive": {"dilution": 0.005}, "negative": {"dilution": 1.0}},
    "sample": {
        "SA01": {"dilution": 1.0, "Barcode": "BC_111", "Concentration": 0.0125},
        "SA02": {"dilution": 2.0, "Barcode": "BC_222"},
        "SA03": {"dilution": 3.0, "Barcode": "BC_333"},
        "SA04": {"dilution": 4.0, "Barcode": "BC_444"},
    },
}

# Generate the Batch object(s)
batch = Batch()
batch.runs = [run_test]
batch.name = "python batch"
batch.properties["PropertyName"] = "Property Value"

# Execute save api
saved_batch = save_batch(server_context, assay_id, batch)
