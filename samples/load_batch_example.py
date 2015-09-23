# Sample to get a batch

from labkey.utils import create_server_context
from labkey.experiment import load_batch

print("Create a server context")
project_name = 'ModuleAssayTest'  # Project folder name
server_context = create_server_context('localhost:8080', project_name, 'labkey', use_ssl=False)

print("Load an Assay batch from the server")
assay_id = 1168  # provide one from your server
batch_id = 95  # provide one from your server
run_group = load_batch(server_context, assay_id, batch_id)

if run_group is not None:
    print("Batch Id: " + str(run_group.id))
    print("Created By: " + run_group.created_by)

