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
# Sample to get a batch

from labkey.utils import create_server_context
from labkey.experiment import load_batch

print("Create a server context")
project_name = 'ModuleAssayTest'  # Project folder name
server_context = create_server_context('localhost:8080', project_name, 'labkey', use_ssl=False)

print("Load an Assay batch from the server")
assay_id = 2809  # provide one from your server
batch_id = 120  # provide one from your server
run_group = load_batch(server_context, assay_id, batch_id)

if run_group is not None:
    print("Batch Id: " + str(run_group.id))
    print("Created By: " + run_group.created_by)

