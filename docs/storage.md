# LabKey Storage API Support

Create, update, or delete a LabKey Freezer Manager storage item. 

Storage items can be used in the creation of a freezer hierarchy. Freezer hierarchies consist of a top level Freezer, 
which can have any combination of child non-terminal storage locations (i.e. those that do not directly contain samples 
but can contain other units) and terminal storage locations (i.e. units in the freezer that directly contain samples 
and cannot contain other units).

Storage items can be of the following types: Physical Location, Freezer, Shelf, Rack, Canister, Storage Unit Type, or 
Terminal Storage Location.

The specific set of props will differ for each storage item type:
- Physical Location: name, description, locationId (rowId of the parent Physical Location)
- Freezer: name, description, locationId (rowId of the parent Physical Location), manufacturer, freezerModel, temperature, temperatureUnits, serialNumber, sensorName, lossRate, status
- Shelf/Rack/Canister: name, description, locationId (rowId of the parent freezer or Shelf/Rack/Canister)
- Storage Unit Type: name, description, unitType (one of the following: "Box", "Plate", "Bag", "Cane", "Tube Rack"), rows, cols (required if positionFormat is not "Num"), positionFormat (one of the following: "Num", "AlphaNum", "AlphaAlpha", "NumAlpha", "NumNum"), positionOrder (one of the following: "RowColumn", "ColumnRow")
- Terminal Storage Location: name, description, typeId (rowId of the Storage Unit Type), locationId (rowId of the parent freezer or Shelf/Rack/Canister)

### Installation and Setup for the LabKey Python API:
- https://github.com/LabKey/labkey-api-python/blob/master/README.md

### Additional details from Labkey Documentation:
- https://www.labkey.org/SampleManagerHelp/wiki-page.view?name=createFreezer
- https://www.labkey.org/SampleManagerHelp/wiki-page.view?name=freezerLocation

### Examples

```python
from labkey.api_wrapper import APIWrapper

labkey_server = "localhost:8080"
project_name = "FM API Test"  # Project folder name
contextPath = "labkey"
api = APIWrapper(labkey_server, project_name, contextPath, use_ssl=False)


###############
# Create a freezer with two shelves
###############
result = api.storage.create_storage_item(
    "Freezer",
    {
        "name": "Freezer #1",
        "description": "Test freezer from API",
        "serialNumber": "ABC123",
        "status": "Active",
    },
)
if result is not None:
    print(result)
else:
    print("Create freezer: no results returned")
    exit()
freezer_row_id = result["data"]["rowId"]

result = api.storage.create_storage_item(
    "Shelf",
    {
        "name": "Shelf #1",
        "description": "This shelf is for samples from Lab A.",
        "locationId": freezer_row_id,
    },
)
if result is not None:
    print(result)
else:
    print("Create shelf: no results returned")
    exit()
shelf1_row_id = result["data"]["rowId"]

result = api.storage.create_storage_item(
    "Shelf",
    {
        "name": "Shelf #2",
        "description": "This shelf is for samples from Lab B.",
        "locationId": freezer_row_id,
    },
)
if result is not None:
    print(result)
else:
    print("Create shelf: no results returned")
    exit()
shelf2_row_id = result["data"]["rowId"]

###############
# Create a terminal storage location in the freezer
###############
result = api.storage.create_storage_item(
    "Storage Unit Type", {"name": "10 X 10 Box", "unitType": "Box", "rows": 10, "cols": 10}
)
if result is not None:
    print(result)
else:
    print("Create storage unit type: no results returned")
    exit()
box_type_id = result["data"]["rowId"]

result = api.storage.create_storage_item(
    "Terminal Storage Location",
    {"name": "Box #1", "typeId": box_type_id, "locationId": shelf1_row_id},
)
if result is not None:
    print(result)
else:
    print("Create box: no results returned")
    exit()
box_id = result["data"]["rowId"]

###############
# Update the location of a box in the freezer
###############
result = api.storage.update_storage_item(
    "Terminal Storage Location", {"rowId": box_id, "locationId": shelf2_row_id}
)
if result is not None:
    print(result)
else:
    print("Update box: no results returned")
    exit()

###############
# Delete the freezer, which will delete the full hierarchy of non-terminal and terminal storage locations
###############
result = api.storage.delete_storage_item("Freezer", freezer_row_id)
if result is not None:
    print(result)
else:
    print("Delete freezer: no results returned")
    exit()
```