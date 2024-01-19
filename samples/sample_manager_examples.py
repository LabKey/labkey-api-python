from labkey.api_wrapper import APIWrapper
from labkey.query import QueryFilter, AuditBehavior
from datetime import datetime

project_name = "home" # LabKey project name
labkey_server = "localhost:8080"
api = APIWrapper(labkey_server, project_name, use_ssl=False)

user = api.security.who_am_i()
storage_plate_type = "96 Well Plate"
parent_location_path = "Freezer1 / Shelf #1 / Rack #1"
plate_name = "Plate #1"
well_location_row = 1 # A = 1, B = 2, etc.
well_location_col = 1

# register/create a sample single sample in the existing "Blood" sample type
sample = {
    "Name": "Sample-1",
    "DrawDate": "2024-01-10",
    "StoredAmount": 10,
    "Units": "mL",
}
sample_response = api.query.insert_rows("samples", "Blood", [sample], audit_behavior=AuditBehavior.DETAILED, audit_user_comment="Creating sample via python API")
# the response object will include the sample metadata including the primary key (rowid)
sample_rowid = sample_response["rows"][0]["rowid"]
print("Successfully created sample: RowId: " + str(sample_rowid) + ", Name: " + sample["Name"])

# query LabKey to see if the plate already exists in the system
plate_rowid = -1
plate_response = api.query.select_rows("inventory", "Box", columns=",".join(["RowId", "Name"]), filter_array=[QueryFilter("Name", plate_name)])
if len(plate_response["rows"]) == 1:
    plate_rowid = plate_response["rows"][0]["RowId"]
    print("Found existing plate: RowId: " + str(plate_rowid) + ", Name: " + plate_name)
else:
    # query LabKey to get the RowIds for the plate type and parent location for the new plate
    storage_plate_type_rowid = api.query.select_rows("inventory", "BoxType", columns=",".join(["RowId"]), filter_array=[QueryFilter("Name", storage_plate_type)])["rows"][0]["RowId"]
    storage_parent_rowid = api.query.select_rows("inventory", "Location", columns=",".join(["RowId"]), filter_array=[QueryFilter("LocationPathDisplay", parent_location_path)])["rows"][0]["RowId"]
    # create the new plate
    plate_response = api.storage.create_storage_item(
        "Terminal Storage Location",
        {"name": plate_name, "typeId": storage_plate_type_rowid, "locationId": storage_parent_rowid},
    )
    plate_rowid = plate_response["data"]["rowId"]
    print("Successfully created plate: RowId: " + str(plate_rowid) + ", Name: " + plate_name)

# assign storage location in the plate for the sample
assign_storage = {
    "materialId": sample_rowid,
    "boxId": plate_rowid,
    "row": well_location_row,
    "col": well_location_col,
}
assign_storage_response = api.query.insert_rows("inventory", "Item", [assign_storage])
print("Successfully assigned storage location for sample: RowId: " + str(sample_rowid) + ", Name: " + sample["Name"] + ", Plate: " + plate_name + ", Row: " + str(assign_storage["row"]) + ", Col: " + str(assign_storage["col"]))

# example of a sample derivation (i.e. from a Blood sample to create 2 child Plasma samples)
child_sample1 = {
    "Name": sample["Name"] + "-D1",
    "MaterialInputs/Blood": sample["Name"],
    "StoredAmount": 5
}
child_sample2 = {
    "Name": sample["Name"] + "-D2",
    "MaterialInputs/Blood": sample["Name"],
    "StoredAmount": 5
}
derivation_response = api.query.insert_rows("samples", "Plasma", [child_sample1, child_sample2], audit_behavior=AuditBehavior.DETAILED, audit_user_comment="Deriving samples via python API")
print("Successfully derived samples: " + child_sample1["Name"] + ", " + child_sample2["Name"] + ", From: " + sample["Name"])
# add derivatives to the plate
child_sample1_rowid = derivation_response["rows"][0]["rowid"]
assign_storage1 = {
    "materialId": child_sample1_rowid,
    "boxId": plate_rowid,
    "row": well_location_row,
    "col": well_location_col + 1,
}
child_sample2_rowid = derivation_response["rows"][1]["rowid"]
assign_storage2 = {
    "materialId": child_sample2_rowid,
    "boxId": plate_rowid,
    "row": well_location_row,
    "col": well_location_col + 2,
}
assign_storage_response = api.query.insert_rows("inventory", "Item", [assign_storage1, assign_storage2])
print("Successfully assigned storage location for sample: RowId: " + str(child_sample1_rowid) + ", Name: " + child_sample1["Name"] + ", Plate: " + plate_name + ", Row: " + str(assign_storage1["row"]) + ", Col: " + str(assign_storage1["col"]))
print("Successfully assigned storage location for sample: RowId: " + str(child_sample2_rowid) + ", Name: " + child_sample2["Name"] + ", Plate: " + plate_name + ", Row: " + str(assign_storage2["row"]) + ", Col: " + str(assign_storage2["col"]))

# example of a sample aliquot (i.e. from a Blood sample to create 2 child Blood samples)
aliquot_sample1 = {
    "Name": sample["Name"] + "-A1",
    "AliquotedFrom": sample["Name"],
    "StoredAmount": 5
}
aliquot_sample2 = {
    "Name": sample["Name"] + "-A2",
    "AliquotedFrom": sample["Name"],
    "StoredAmount": 5
}
aliquot_response = api.query.insert_rows("samples", "Blood", [aliquot_sample1, aliquot_sample2], audit_behavior=AuditBehavior.DETAILED, audit_user_comment="Aliquoting samples via python API")
print("Successfully aliquoted samples: " + aliquot_sample1["Name"] + ", " + aliquot_sample2["Name"] + ", From: " + sample["Name"])
# add aliquots to the plate
aliquot_sample1_rowid = aliquot_response["rows"][0]["rowid"]
assign_storage1 = {
    "materialId": aliquot_sample1_rowid,
    "boxId": plate_rowid,
    "row": well_location_row,
    "col": well_location_col + 3,
}
aliquot_sample2_rowid = aliquot_response["rows"][1]["rowid"]
assign_storage2 = {
    "materialId": aliquot_sample2_rowid,
    "boxId": plate_rowid,
    "row": well_location_row,
    "col": well_location_col + 4,
}
assign_storage_response = api.query.insert_rows("inventory", "Item", [assign_storage1, assign_storage2])
print("Successfully assigned storage location for sample: RowId: " + str(aliquot_sample1_rowid) + ", Name: " + aliquot_sample1["Name"] + ", Plate: " + plate_name + ", Row: " + str(assign_storage1["row"]) + ", Col: " + str(assign_storage1["col"]))
print("Successfully assigned storage location for sample: RowId: " + str(aliquot_sample2_rowid) + ", Name: " + aliquot_sample2["Name"] + ", Plate: " + plate_name + ", Row: " + str(assign_storage2["row"]) + ", Col: " + str(assign_storage2["col"]))

# we need the RowId for the inventory.Item row of the sample in order to check it out / check it in
aliquot_storage1_rowid = assign_storage_response["rows"][0]["rowid"]
aliquot_storage2_rowid = assign_storage_response["rows"][1]["rowid"]

# checking 2 aliquot samples out of storage
toUpdate = [
   {"rowId": aliquot_storage1_rowid, "checkedOutBy": user.id, "checkedOut": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
   {"rowId": aliquot_storage2_rowid, "checkedOutBy": user.id, "checkedOut": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
]
checkout_response = api.query.update_rows("inventory", "Item", toUpdate, audit_behavior=AuditBehavior.DETAILED, audit_user_comment="Checking out samples via python API")
print("Successfully checked out samples: " + aliquot_sample1["Name"] + ", " + aliquot_sample2["Name"])

# checking 2 aliquot samples back into storage
toUpdate = [
    {"rowId": aliquot_storage1_rowid, "checkedOutBy": None, "checkedOut": None},
    {"rowId": aliquot_storage2_rowid, "checkedOutBy": None, "checkedOut": None},
]
checkin_response = api.query.update_rows("inventory", "Item", toUpdate, audit_behavior=AuditBehavior.DETAILED, audit_user_comment="Checking in samples via python API")
print("Successfully checked in samples: " + aliquot_sample1["Name"] + ", " + aliquot_sample2["Name"])

# move the plate to a new location (i.e. from "Shelf #1 / Rack #1" to "Bench")
new_parent_location_path = "Freezer1 / Bench"
new_storage_parent_rowid = api.query.select_rows("inventory", "Location", columns=",".join(["RowId"]), filter_array=[QueryFilter("LocationPathDisplay", new_parent_location_path)])["rows"][0]["RowId"]
if new_storage_parent_rowid is None:
    print("Failed to find new parent location: " + new_parent_location_path)
else:
    toUpdate = [
        {"rowId": plate_rowid, "locationId": new_storage_parent_rowid},
    ]
    move_response = api.query.update_rows("inventory", "Box", toUpdate, audit_behavior=AuditBehavior.DETAILED, audit_user_comment="Moving plate via python API")
    print("Successfully moved plate: " + plate_name + ", From: " + parent_location_path + ", To: " + new_parent_location_path)
