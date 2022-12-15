#
# Copyright (c) 2017-2018 LabKey Corporation
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
############################################################################
NAME:
LabKey Storage API

SUMMARY:
This module provides functions for interacting with storage items on a LabKey Server.

DESCRIPTION:
Create, update, or delete a LabKey Freezer Manager storage item. Storage items can be used in the creation of a
storage hierarchy. Storage hierarchies consist of a top level Freezer or Primary Storage location, which can have any
combination of child non-terminal storage locations (i.e. those that do not directly contain samples but can contain
other units) and terminal storage locations (i.e. units in the storage that directly contain samples and cannot contain
other units).

Storage items can be of the following types: Physical Location, Freezer, Primary Storage, Shelf, Rack, Canister, Storage Unit Type, or Terminal Storage Location.
The specific set of props will differ for each storage item type:
 - Physical Location: name, description, locationId (rowId of the parent Physical Location)
 - Freezer: name, description, locationId (rowId of the parent Physical Location), manufacturer, freezerModel, temperature, temperatureUnits, serialNumber, sensorName, lossRate, status
 - Primary Storage: name, description, locationId (rowId of the parent Physical Location), temperatureControlled (boolean)
 - Shelf/Rack/Canister: name, description, locationId (rowId of the parent freezer, primary storage, or Shelf/Rack/Canister)
 - Storage Unit Type: name, description, unitType (one of the following: "Box", "Plate", "Bag", "Cane", "Tube Rack"), rows, cols (required if positionFormat is not "Num"), positionFormat (one of the following: "Num", "AlphaNum", "AlphaAlpha", "NumAlpha", "NumNum"), positionOrder (one of the following: "RowColumn", "ColumnRow")
 - Terminal Storage Location: name, description, typeId (rowId of the Storage Unit Type), locationId (rowId of the parent freezer, primary storage, or Shelf/Rack/Canister)

Installation and Setup for the LabKey Python API:
https://github.com/LabKey/labkey-api-python/blob/master/README.md

Additional details from Labkey Documentation:
https://www.labkey.org/SampleManagerHelp/wiki-page.view?name=createFreezer
https://www.labkey.org/SampleManagerHelp/wiki-page.view?name=freezerLocation

############################################################################
"""
import functools
from dataclasses import dataclass

from typing import Union, List

from labkey.server_context import ServerContext

STORAGE_CONTROLLER = "storage"


def create_storage_item(
    server_context: ServerContext, type: str, props: dict, container_path: str = None
):
    """
    Create a new LabKey Freezer Manager storage item that can be used in the creation of a storage hierarchy.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param type:
    :param props:
    :param container_path:
    :return:
    """
    url = server_context.build_url(STORAGE_CONTROLLER, "create.api", container_path)
    payload = {"type": type, "props": props}

    return server_context.make_request(url, json=payload)


def update_storage_item(
    server_context: ServerContext, type: str, props: dict, container_path: str = None
):
    """
    Update an existing LabKey Freezer Manager storage item to change its properties or location within the storage hierarchy.
    For update_storage_item, the "rowId" primary key value is required to be set within the props.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param type:
    :param props:
    :param container_path:
    :return:
    """
    url = server_context.build_url(STORAGE_CONTROLLER, "update.api", container_path)
    payload = {"type": type, "props": props}

    return server_context.make_request(url, json=payload)


def delete_storage_item(
    server_context: ServerContext, type: str, row_id: int, container_path: str = None
):
    """
    Delete an existing LabKey Freezer Manager storage item. Note that deletion of freezers, primary storage, or locations
    within the storage hierarchy will cascade the delete down the hierarchy to remove child locations and terminal
    storage locations. Samples in the deleted storage location(s) will not be deleted but will be removed from storage.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param type:
    :param row_id:
    :param container_path:
    :return:
    """
    url = server_context.build_url(STORAGE_CONTROLLER, "delete.api", container_path)
    payload = {"type": type, "props": {"rowId": row_id}}

    return server_context.make_request(url, json=payload)


class StorageWrapper:
    """
    Wrapper for all of the API methods exposed in the storage module. Used by the APIWrapper class.
    """

    def __init__(self, server_context: ServerContext):
        self.server_context = server_context

    @functools.wraps(create_storage_item)
    def create_storage_item(self, type: str, props: dict, container_path: str = None):
        return create_storage_item(self.server_context, type, props, container_path)

    @functools.wraps(update_storage_item)
    def update_storage_item(self, type: str, props: dict, container_path: str = None):
        return update_storage_item(self.server_context, type, props, container_path)

    @functools.wraps(delete_storage_item)
    def delete_storage_item(self, type: str, row_id: int, container_path: str = None):
        return delete_storage_item(self.server_context, type, row_id, container_path)
