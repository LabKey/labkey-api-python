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
import pytest

from labkey.experiment import load_batch, save_batch, Batch, Run
from labkey.exceptions import (
    RequestError,
    QueryNotFoundError,
    ServerNotFoundError,
    RequestAuthorizationError,
)

from .utilities import MockLabKey, mock_server_context, success_test, throws_error_test


class MockLoadBatch(MockLabKey):
    api = "getAssayBatch.api"
    default_action = "assay"
    default_success_body = {
        "assayId": 2809,
        "batch": {
            "lsid": "urn:lsid:labkey.com:Experiment.Folder-1721:465ad7db-58d8-1033-a587-7eb0c02c2efe",
            "createdBy": "",
            "created": "2015/10/19 18:21:57",
            "name": "python batch",
            "modified": "2015/10/19 18:21:57",
            "modifiedBy": "",
            "comment": None,
            "id": 120,
            "runs": [
                {
                    "dataOutputs": [],
                    "dataRows": [
                        {
                            "Treatment Group": None,
                            "Start Date": None,
                            "Height _inches_": None,
                            "Comments": None,
                            "Status of Infection": None,
                            "Country": None,
                            "Gender": None,
                            "Group Assignment": None,
                            "Participant ID": None,
                            "Date": None,
                        },
                        {
                            "Treatment Group": None,
                            "Start Date": None,
                            "Height _inches_": None,
                            "Comments": None,
                            "Status of Infection": None,
                            "Country": None,
                            "Gender": None,
                            "Group Assignment": None,
                            "Participant ID": None,
                            "Date": None,
                        },
                        {
                            "Treatment Group": None,
                            "Start Date": None,
                            "Height _inches_": None,
                            "Comments": None,
                            "Status of Infection": None,
                            "Country": None,
                            "Gender": None,
                            "Group Assignment": None,
                            "Participant ID": None,
                            "Date": None,
                        },
                    ],
                    "dataInputs": [],
                    "created": "2015/10/19 18:21:57",
                    "materialInputs": [
                        {
                            "lsid": "urn:lsid:labkey.com:AssayRunMaterial.Folder-1721:Unknown",
                            "role": "Sample",
                            "created": "2015/10/19 18:21:57",
                            "name": "Unknown",
                            "modified": "2015/10/19 18:21:57",
                            "id": 7641,
                        }
                    ],
                    "lsid": "urn:lsid:labkey.com:GeneralAssayRun.Folder-1721:465ad7dd-58d8-1033-a587-7eb0c02c2efe",
                    "materialOutputs": [],
                    "createdBy": "",
                    "name": "python upload",
                    "modified": "2015/10/19 18:21:57",
                    "modifiedBy": "",
                    "comment": None,
                    "id": 1526,
                    "properties": {},
                }
            ],
            "properties": {"ParticipantVisitResolver": None, "TargetStudy": None},
        },
    }


class MockSaveBatch(MockLabKey):
    api = "saveAssayBatch.api"
    default_action = "assay"
    default_success_body = {
        "batches": [
            {
                "lsid": "urn:lsid:labkey.com:Experiment.Folder-1721:50666e45-609f-1033-ba4a-ca4935e31f28",
                "createdBy": "",
                "created": "2015/10/29 12:17:50",
                "name": "python batch 7",
                "modified": "2015/10/29 12:17:51",
                "modifiedBy": "",
                "comment": None,
                "id": 139,
                "runs": [
                    {
                        "dataOutputs": [],
                        "dataRows": [
                            {
                                "Treatment Group": None,
                                "Start Date": None,
                                "Height _inches_": None,
                                "Comments": None,
                                "Status of Infection": None,
                                "Country": None,
                                "Gender": None,
                                "Group Assignment": None,
                                "Participant ID": None,
                                "Date": None,
                            },
                            {
                                "Treatment Group": None,
                                "Start Date": None,
                                "Height _inches_": None,
                                "Comments": None,
                                "Status of Infection": None,
                                "Country": None,
                                "Gender": None,
                                "Group Assignment": None,
                                "Participant ID": None,
                                "Date": None,
                            },
                            {
                                "Treatment Group": None,
                                "Start Date": None,
                                "Height _inches_": None,
                                "Comments": None,
                                "Status of Infection": None,
                                "Country": None,
                                "Gender": None,
                                "Group Assignment": None,
                                "Participant ID": None,
                                "Date": None,
                            },
                        ],
                        "dataInputs": [],
                        "created": "2015/10/29 12:17:50",
                        "materialInputs": [
                            {
                                "lsid": "urn:lsid:labkey.com:AssayRunMaterial.Folder-1721:Unknown",
                                "role": "Sample",
                                "created": "2015/10/19 18:21:57",
                                "name": "Unknown",
                                "modified": "2015/10/19 18:21:57",
                                "id": 7641,
                            }
                        ],
                        "lsid": "urn:lsid:labkey.com:GeneralAssayRun.Folder-1721:50666e47-609f-1033-ba4a-ca4935e31f28",
                        "materialOutputs": [],
                        "createdBy": "",
                        "name": "python upload",
                        "modified": "2015/10/29 12:17:51",
                        "modifiedBy": "",
                        "comment": None,
                        "id": 1673,
                        "properties": {},
                    }
                ],
                "properties": {"ParticipantVisitResolver": None, "TargetStudy": None},
            }
        ],
        "assayId": 2809,
    }


assay_id = 12345
batch_id = 54321


@pytest.fixture
def load_batch_setup():
    service = MockLoadBatch()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": '{"assayId": 12345, "batchId": 54321}',
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), assay_id, batch_id]
    return service, args, expected_kwargs


def test_load_batch_success(load_batch_setup):
    service, args, expected_kwargs = load_batch_setup
    success_test(service.get_successful_response(), load_batch, False, *args, **expected_kwargs)


def test_load_batch_unauthorized(load_batch_setup):
    service, args, expected_kwargs = load_batch_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        load_batch,
        *args,
        **expected_kwargs,
    )


def test_load_batch_query_not_found(load_batch_setup):
    service, args, expected_kwargs = load_batch_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        load_batch,
        *args,
        **expected_kwargs,
    )


def test_load_batch_server_not_found(load_batch_setup):
    service, args, expected_kwargs = load_batch_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        load_batch,
        *args,
        **expected_kwargs,
    )


def test_load_batch_general_error(load_batch_setup):
    service, args, expected_kwargs = load_batch_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), load_batch, *args, **expected_kwargs
    )


@pytest.fixture
def save_batch_setup():
    data_rows = []

    # Generate the Run object(s)
    run = Run()
    run.name = "python upload"
    run.data_rows = data_rows
    run.properties["RunFieldName"] = "Run Field Value"

    # Generate the Batch object(s)
    batch = Batch()
    batch.runs = [run]
    batch.properties["PropertyName"] = "Property Value"

    service = MockSaveBatch()
    expected_kwargs = {
        "expected_args": [service.get_server_url()],
        "data": '{"assayId": 12345, "batches": [{"batchProtocolId": null, "comment": null, "created": null, "createdBy": null, "modified": null, "modifiedBy": null, "name": null, "properties": {"PropertyName": "Property Value"}, "runs": [{"name": "python upload", "properties": {"RunFieldName": "Run Field Value"}}]}]}',
        "headers": {"Content-Type": "application/json"},
        "timeout": 300,
        "allow_redirects": False,
    }
    args = [mock_server_context(service), assay_id, batch]
    return service, args, expected_kwargs


def test_save_batch_success(save_batch_setup):
    service, args, expected_kwargs = save_batch_setup
    success_test(service.get_successful_response(), save_batch, False, *args, **expected_kwargs)


def test_save_batch_unauthorized(save_batch_setup):
    service, args, expected_kwargs = save_batch_setup
    throws_error_test(
        RequestAuthorizationError,
        service.get_unauthorized_response(),
        save_batch,
        *args,
        **expected_kwargs,
    )


def test_save_batch_query_not_found(save_batch_setup):
    service, args, expected_kwargs = save_batch_setup
    throws_error_test(
        QueryNotFoundError,
        service.get_query_not_found_response(),
        save_batch,
        *args,
        **expected_kwargs,
    )


def test_save_batch_server_not_found(save_batch_setup):
    service, args, expected_kwargs = save_batch_setup
    throws_error_test(
        ServerNotFoundError,
        service.get_server_not_found_response(),
        save_batch,
        *args,
        **expected_kwargs,
    )


def test_save_batch_general_error(save_batch_setup):
    service, args, expected_kwargs = save_batch_setup
    throws_error_test(
        RequestError, service.get_general_error_response(), save_batch, *args, **expected_kwargs
    )
