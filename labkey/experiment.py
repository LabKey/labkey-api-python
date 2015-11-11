#
# Copyright (c) 2015 LabKey Corporation
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
import json

from requests.exceptions import SSLError
from labkey.utils import build_url, handle_response
from labkey.exceptions import ServerContextError


# EXAMPLE
# -------

# from utils import create_server_context
# from experiment import load_batch, save_batch
#
# print("Create a server context")
# server_context = create_server_context('localhost:8080', 'CDSTest Project', 'labkey', use_ssl=False)
#
# print("Load an Assay batch from the server")
# assay_id = # provide one from your server
# batch_id = # provide one from your server
# run_group = load_batch(server_context, assay_id, batch_id)
#
# if run_group is not None:
# 	print("Batch Id: " + str(run_group.id))
# 	print("Created By: " + run_group.created_by)
#
# 	print("Modify a property")
# 	batch_property_name = '' # provide one from your assay
# 	batch_property_value = '' # provide one
# 	run_group.properties[batch_property_name] = batch_property_value
#
# 	print("Save the batch")
# 	save_batch(server_context, assay_id, run_group)

# --------
# /EXAMPLE


# TODO Incorporate logging
def load_batch(server_context, assay_id, batch_id):
    """
    Loads a batch from the server.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param assay_id: The protocol id of the assay from which to load a batch.
    :param batch_id:
    :return:
    """
    load_batch_url = build_url(server_context, 'assay', 'getAssayBatch.api')
    session = server_context['session']
    loaded_batch = None

    payload = {
        'assayId': assay_id,
        'batchId': batch_id
    }

    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    try:
        response = session.post(load_batch_url, data=json.dumps(payload, sort_keys=True), headers=headers)
        json_body = handle_response(response)
        if json_body is not None:
            loaded_batch = Batch.from_data(json_body['batch'])
    except SSLError as e:
        raise ServerContextError(e)

    return loaded_batch


def save_batch(server_context, assay_id, batch):
    """
    Saves a modified batch.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param assay_id: The assay protocol id.
    :param batch: The Batch to save.
    :return:
    """
    result = save_batches(server_context, assay_id, [batch])

    if result is not None:
        return result[0]
    return None


def save_batches(server_context, assay_id, batches):
    """
    Saves a modified batches.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param assay_id: The assay protocol id.
    :param batches: The Batch(es) to save.
    :return:
    """

    save_batch_url = build_url(server_context, 'assay', 'saveAssayBatch.api')
    session = server_context['session']

    json_batches = []
    if batches is None:
        return None  # Nothing to save

    for batch in batches:
        if isinstance(batch, Batch):
            json_batches.append(batch.to_json())
        else:
            raise Exception('save_batch() "batches" expected to be a set Batch instances')

    payload = {
        'assayId': assay_id,
        'batches': json_batches
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    try:
        # print(payload)
        response = session.post(save_batch_url, data=json.dumps(payload, sort_keys=True), headers=headers)
        json_body = handle_response(response)
        if json_body is not None:
            resp_batches = json_body['batches']
            return [Batch.from_data(resp_batch) for resp_batch in resp_batches]
    except SSLError as e:
        raise ServerContextError(e)

    return None


class ExpObject(object):
    def __init__(self, **kwargs):
        self.lsid = kwargs.pop('lsid', None)  # Life Science identifier
        self.name = kwargs.pop('name', None)
        self.id = kwargs.pop('id', 0)
        self.row_id = self.id
        self.comment = kwargs.pop('comment', None)
        self.created = kwargs.pop('created', None)
        self.modified = kwargs.pop('modified', None)
        self.created_by = kwargs.pop('created_by', kwargs.pop('createdBy', None))
        self.modified_by = kwargs.pop('modified_by', kwargs.pop('modifiedBy', None))
        self.properties = kwargs.pop('properties', {})

    def to_json(self):
        data = {
            # 'id': self.id,
            'lsid': self.lsid,
            'comment': self.comment,
            'name': self.name,
            'created': self.created,
            'createdBy': self.created_by,
            'modified': self.modified,
            'modifiedBy': self.modified_by,
            'properties': self.properties
        }
        return data


# TODO: Move these classes into their own file(s)
class Batch(ExpObject):
    def __init__(self, **kwargs):
        super(Batch, self).__init__(**kwargs)

        self.batch_protocol_id = kwargs.pop('batch_protocol_id', self.id)
        self.hidden = kwargs.pop('hidden', False)

        runs = kwargs.pop('runs', [])
        run_instances = []

        for run in runs:
            run_instances.append(Run.from_data(run))

        self.runs = run_instances

    @staticmethod
    def from_data(data):
        return Batch(**data)

    def to_json(self):

        data = super(Batch, self).to_json()

        data['batchProtocolId'] = self.batch_protocol_id

        json_runs = []
        for run in self.runs:
            json_runs.append(run.to_json())

        # The JavaScript API doesn't appear to send these?
        # data['batchProtocolId'] = self.batch_protocol_id
        # data['hidden'] = self.hidden
        data['runs'] = json_runs

        return data


class Run(ExpObject):
    def __init__(self, **kwargs):
        super(Run, self).__init__(**kwargs)

        self.experiments = kwargs.pop('experiments', [])
        self.file_path_root = kwargs.pop('file_path_root', kwargs.pop('filePathRoot', None))
        self.protocol = kwargs.pop('protocol', None)
        self.data_outputs = kwargs.pop('data_outputs', kwargs.pop('dataOutputs', []))
        self.data_rows = kwargs.pop('data_rows', kwargs.pop('dataRows', []))
        self.material_inputs = kwargs.pop('material_inputs', kwargs.pop('materialInputs', []))
        self.material_outputs = kwargs.pop('material_outputs', kwargs.pop('materialOutputs', []))
        self.object_properties = kwargs.pop('object_properties', kwargs.pop('objectProperties', []))

        # TODO: initialize protocol
        # self._protocol = None

        # initialize data_inputs
        data_inputs = kwargs.pop('data_inputs', kwargs.pop('dataInputs', []))
        data_inputs_instances = []

        for input in data_inputs:
            data_inputs_instances.append(Data.from_data(input))

        self.data_inputs = data_inputs_instances

    @staticmethod
    def from_data(data):
        return Run(**data)

    def to_json(self):
        data = super(Run, self).to_json()

        data['dataInputs'] = [data_input.to_json() for data_input in self.data_inputs]
        data['dataRows'] = self.data_rows
        data['experiments'] = self.experiments
        data['filePathRoot'] = self.file_path_root
        data['materialInputs'] = self.material_inputs
        data['materialOutputs'] = self.material_outputs

        return data


class ProtocolOutput(ExpObject):
    def __init__(self, **kwargs):
        super(ProtocolOutput, self).__init__(**kwargs)

        self.source_protocol = kwargs.pop('source_protocol', kwargs.pop('sourceProtocol', None))
        self.run = kwargs.pop('run', None)  # TODO Check if this should be a Run instance
        self.target_applications = kwargs.pop('target_applications', kwargs.pop('targetApplications', None))
        self.successor_runs = kwargs.pop('successor_runs', kwargs.pop('successorRuns', kwargs.pop('sucessorRuns', None)))  # sic
        self.cpas_type = kwargs.pop('cpas_type', kwargs.pop('cpasType', None))

    @staticmethod
    def from_data(data):
        return ProtocolOutput(**data)

    def to_json(self):
        data = super(ProtocolOutput, self).to_json()

        data['sourceProtocol'] = self.source_protocol
        data['run'] = self.run
        data['targetApplications'] = self.target_applications
        data['sucessorRuns'] = self.successor_runs
        data['cpasType'] = self.cpas_type

        return data


class Data(ProtocolOutput):
    def __init__(self, **kwargs):
        super(Data, self).__init__(**kwargs)

        self.data_type = kwargs.pop('data_type', kwargs.pop('dataType', None))
        self.data_file_url = kwargs.pop('data_file_url', kwargs.pop('dataFileURL', None))
        self.pipeline_path = kwargs.pop('pipeline_path', kwargs.pop('pipelinePath', None))
        self.role = kwargs.pop('role', None)

    @staticmethod
    def from_data(data):
        return Data(**data)

    def to_json(self):
        data = super(Data, self).to_json()

        data['dataFileURL'] = self.data_file_url
        data['dataType'] = self.data_type
        data['pipelinePath'] = self.pipeline_path
        data['role'] = self.role

        return data
