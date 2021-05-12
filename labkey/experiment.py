#
# Copyright (c) 2015-2018 LabKey Corporation
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
import functools
from typing import List, Optional

from .server_context import ServerContext


class ExpObject:
    def __init__(self, **kwargs):
        self.lsid = kwargs.pop("lsid", None)  # Life Science identifier
        self.name = kwargs.pop("name", None)
        self.id = kwargs.pop("id", None)
        self.row_id = self.id
        self.comment = kwargs.pop("comment", None)
        self.created = kwargs.pop("created", None)
        self.modified = kwargs.pop("modified", None)
        self.created_by = kwargs.pop("created_by", kwargs.pop("createdBy", None))
        self.modified_by = kwargs.pop("modified_by", kwargs.pop("modifiedBy", None))
        self.properties = kwargs.pop("properties", {})

    def to_json(self):
        data = {
            # 'id': self.id,
            "comment": self.comment,
            "name": self.name,
            "created": self.created,
            "createdBy": self.created_by,
            "modified": self.modified,
            "modifiedBy": self.modified_by,
            "properties": self.properties,
        }

        if self.id is not None:
            data.update({"id": self.id})

        if self.lsid is not None:
            data.update({"lsid": self.lsid})

        return data


class Batch(ExpObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch_protocol_id = kwargs.pop("batch_protocol_id", self.id)
        self.hidden = kwargs.pop("hidden", False)
        runs = kwargs.pop("runs", [])
        self.runs = [Run(**run) for run in runs]

    def to_json(self):
        data = super().to_json()
        data["batchProtocolId"] = self.batch_protocol_id

        # The JavaScript API doesn't appear to send these?
        # data['batchProtocolId'] = self.batch_protocol_id
        # data['hidden'] = self.hidden
        data["runs"] = [run.to_json() for run in self.runs]

        return data


class Run(ExpObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.experiments = kwargs.pop("experiments", [])
        self.file_path_root = kwargs.pop("file_path_root", kwargs.pop("filePathRoot", None))
        self.protocol = kwargs.pop("protocol", None)
        self.data_outputs = kwargs.pop("data_outputs", kwargs.pop("dataOutputs", []))
        self.data_rows = kwargs.pop("data_rows", kwargs.pop("dataRows", []))
        self.material_inputs = kwargs.pop("material_inputs", kwargs.pop("materialInputs", []))
        self.material_outputs = kwargs.pop("material_outputs", kwargs.pop("materialOutputs", []))
        self.object_properties = kwargs.pop("object_properties", kwargs.pop("objectProperties", []))
        self.plate_metadata = kwargs.pop("plate_metadata", None)

        # TODO: initialize protocol
        # self._protocol = None

        data_inputs = kwargs.pop("data_inputs", kwargs.pop("dataInputs", []))
        self.data_inputs = [Data(**input_) for input_ in data_inputs]

    def to_json(self):
        data = super().to_json()
        data["dataInputs"] = [data_input.to_json() for data_input in self.data_inputs]
        data["dataRows"] = self.data_rows
        data["experiments"] = self.experiments
        data["filePathRoot"] = self.file_path_root
        data["materialInputs"] = self.material_inputs
        data["materialOutputs"] = self.material_outputs
        data["plateMetadata"] = self.plate_metadata

        # Issue 2489: Drop empty values. Server supplies default values for missing keys,
        # and will throw exception if a null value is supplied
        data = {k: v for k, v in data.items() if v}
        return data


class RunItem(ExpObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_protocol = kwargs.pop("source_protocol", kwargs.pop("sourceProtocol", None))
        self.run = kwargs.pop("run", None)  # TODO Check if this should be a Run instance
        self.target_applications = kwargs.pop(
            "target_applications", kwargs.pop("targetApplications", None)
        )
        self.successor_runs = kwargs.pop(
            "successor_runs",
            kwargs.pop("successorRuns", kwargs.pop("sucessorRuns", None)),
        )  # sic
        self.cpas_type = kwargs.pop("cpas_type", kwargs.pop("cpasType", None))

    def to_json(self):
        data = super().to_json()
        data["sourceProtocol"] = self.source_protocol
        data["run"] = self.run
        data["targetApplications"] = self.target_applications
        data["sucessorRuns"] = self.successor_runs
        data["cpasType"] = self.cpas_type

        return data


class Data(RunItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_type = kwargs.pop("data_type", kwargs.pop("dataType", None))
        self.data_file_url = kwargs.pop("data_file_url", kwargs.pop("dataFileURL", None))
        self.pipeline_path = kwargs.pop("pipeline_path", kwargs.pop("pipelinePath", None))
        self.role = kwargs.pop("role", None)

    def to_json(self):
        data = super().to_json()
        data["dataFileURL"] = self.data_file_url
        data["dataType"] = self.data_type
        data["pipelinePath"] = self.pipeline_path
        data["role"] = self.role

        return data


# TODO Incorporate logging
def load_batch(server_context: ServerContext, assay_id: int, batch_id: int) -> Optional[Batch]:
    """
    Loads a batch from the server.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param assay_id: The protocol id of the assay from which to load a batch.
    :param batch_id:
    :return:
    """
    load_batch_url = server_context.build_url("assay", "getAssayBatch.api")
    loaded_batch = None
    payload = {"assayId": assay_id, "batchId": batch_id}
    json_body = server_context.make_request(load_batch_url, json=payload)

    if json_body is not None:
        loaded_batch = Batch(**json_body["batch"])

    return loaded_batch


def save_batch(server_context: ServerContext, assay_id: int, batch: Batch) -> Optional[Batch]:
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


def save_batches(
    server_context: ServerContext, assay_id: int, batches: List[Batch]
) -> Optional[List[Batch]]:
    """
    Saves a modified batches.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param assay_id: The assay protocol id.
    :param batches: The Batch(es) to save.
    :return:
    """
    save_batch_url = server_context.build_url("assay", "saveAssayBatch.api")
    json_batches = []

    if batches is None:
        return None  # Nothing to save

    for batch in batches:
        if isinstance(batch, Batch):
            json_batches.append(batch.to_json())
        else:
            raise Exception('save_batch() "batches" expected to be a set Batch instances')

    payload = {"assayId": assay_id, "batches": json_batches}
    json_body = server_context.make_request(save_batch_url, json=payload)

    if json_body is not None:
        resp_batches = json_body["batches"]
        return [Batch(**resp_batch) for resp_batch in resp_batches]

    return None


class ExperimentWrapper:
    """
    Wrapper for all of the API methods exposed in the experiment module. Used by the APIWrapper class.
    """

    def __init__(self, server_context: ServerContext):
        self.server_context = server_context

    @functools.wraps(load_batch)
    def load_batch(self, assay_id: int, batch_id: int) -> Optional[Batch]:
        return load_batch(self.server_context, assay_id, batch_id)

    @functools.wraps(save_batch)
    def save_batch(self, assay_id: int, batch: Batch) -> Optional[Batch]:
        return save_batch(self.server_context, assay_id, batch)

    @functools.wraps(save_batches)
    def save_batches(self, assay_id: int, batches: List[Batch]) -> Optional[List[Batch]]:
        return save_batches(self.server_context, assay_id, batches)
