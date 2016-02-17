#
# Copyright (c) 2015-2016 LabKey Corporation
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
"""
Examples using the Experiment.py API

Sample code to submit a single batch of Assay data containing a run with three rows of data

"""


from labkey.utils import create_server_context
from labkey.experiment import save_batch, Batch, Run

assay_id = 2809  # provide one from your server. rowid from the URL query parameters

print("Create a server context")
project_name = 'ModuleAssayTest'
server_context = create_server_context('localhost:8080', project_name, 'labkey', use_ssl=False)

# Run data rows
dataRows = [
    {
        # ColumnName : Value
        "SampleId": "Monkey 1",
        "TimePoint": "2008/11/02 11:22:33",
        "DoubleData": 4.5,
        "HiddenData": "another data point"
    }, {
        "SampleId": "Monkey 2",
        "TimePoint": "2008/11/02 14:00:01",
        "DoubleData": 3.1,
        "HiddenData": "fozzy bear"
    }, {
        "SampleId": "Monkey 3",
        "TimePoint": "2008/11/02 14:00:01",
        "DoubleData": 1.5,
        "HiddenData": "jimbo"
    }
]

# Generate the Run object(s)
runTest = Run()
runTest.name = 'python upload'
runTest.data_rows = dataRows
runTest.properties['RunFieldName'] = 'Run Field Value'

# Generate the Batch object(s)
batch = Batch()
batch.runs = [runTest]
batch.name = 'python batch'
batch.properties['PropertyName'] = 'Property Value'

# Execute save api
RESULT = save_batch(server_context, assay_id, batch)
# RESULT = save_batches(server_context, assay_id, [batch1, batch2])
print(RESULT.id)

