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
from labkey.experiment import Batch, Run, load_batch, save_batch

labkey_server = "localhost:8080"
project_name = "ModulesAssayTest"  # Project folder name
context_path = "labkey"
server_context = create_server_context(labkey_server, project_name, context_path, use_ssl=False)

assay_id = 3315  # provide one from your server

###################
# Save an Assay batch
###################

# Generate the Run object(s)
run_test = Run()
run_test.name = "python upload"
run_test.data_rows = [
    {
        # ColumnName: Value
        "SampleId": "Monkey 1",
        "TimePoint": "2008/11/02 11:22:33",
        "DoubleData": 4.5,
        "HiddenData": "another data point",
    },
    {
        "SampleId": "Monkey 2",
        "TimePoint": "2008/11/02 14:00:01",
        "DoubleData": 3.1,
        "HiddenData": "fozzy bear",
    },
    {
        "SampleId": "Monkey 3",
        "TimePoint": "2008/11/02 14:00:01",
        "DoubleData": 1.5,
        "HiddenData": "jimbo",
    },
]
run_test.properties["RunFieldName"] = "Run Field Value"

# Generate the Batch object(s)
batch = Batch()
batch.runs = [run_test]
batch.name = "python batch"
batch.properties["PropertyName"] = "Property Value"

# Execute save api
saved_batch = save_batch(server_context, assay_id, batch)

###################
# Load an Assay batch
###################
batch_id = saved_batch.row_id  # provide one from your server
run_group = load_batch(server_context, assay_id, batch_id)

if run_group is not None:
    print("Batch Id: " + str(run_group.id))
    print("Created By: " + run_group.created_by)
