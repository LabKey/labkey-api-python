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
import json
from functools import wraps
from datetime import date, datetime
import csv


# Issue #14: json.dumps on datetime throws TypeError
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        return super().default(o)


@wraps(json.dumps)
def json_dumps(*args, **kwargs):
    kwargs.setdefault("cls", DateTimeEncoder)
    return json.dumps(*args, **kwargs)


def transform_helper(user_transform_func, file_path_run_properties):
    #file_path_run_properties must be explicitly defined as ${runInfo} within the user's transform script
    #parse run properties to for results data in and out filepaths
    file_path_in = ''
    file_path_out = ''
    with open(file_path_run_properties) as file_run_properties:
        for l in file_run_properties:
            row = l.strip().split('\t')
            if row[0] == 'runDataFile':
                file_path_out = row[3]
            if row[0] == 'runDataUploadedFile':
                file_path_in = row[1]
    
    #parse results data into array, confirming supported file type is used
    with open(file_path_in) as file_in:
        data_grid = []

        for l in file_in:
            if '\t' in l:
                row = l.replace('\n', '').split('\t')
            elif ',' in l:
                row = l.replace('\n', '').split(',')
            else:
                raise ValueError('Unsupported file type or delimiter used. Header used: \n' + str(l))
            data_grid.append(row)    
    
    #run user transform on parsed results data array
    transformed_grid = user_transform_func(data_grid)
    
    #write transformed results data array to LabKey assay results data grid
    #transformed array must be a python list object, not a numpy array or pandas dataframe
    with open(file_path_out, mode='w') as file_out:
        for row in transformed_grid:
            row = [str(el).strip() for el in row]
            row = '\t'.join(row)        
            file_out.write(row + '\n')
   
def bulk_import_freezerpro_storage(
        api,
        file_path
    ):
    data = []
    
    with open(file_path) as freezer_file:
        lines = csv.reader(freezer_file)
        is_header = True
        for line in lines:
            if is_header:
                is_header = False
            else:
                data += [line]
             
    #func uses these dicts to minimize calls to server
    loc_dict = {}
    term_dict = {}
    
    #iterate through list of locations
    for row in data:
        l2_name, l3_name, l4_name, box, box_name = row
        
        #check if l2 location was already created; create it if not
        if l2_name not in loc_dict:
            result = api.storage.create_storage_item(
                'Freezer',
                {
                    'name': l2_name
                }
            )
            loc_dict[l2_name] = result['data']['rowId'] 
            
        #check if l3 location was already created; create it if not
        if l2_name + l3_name not in loc_dict:        
            l3_type = l3_name.split(' ')[0]
            
            result = api.storage.create_storage_item(
                l3_type,
                {
                    'name': l3_name,
                    'locationId': loc_dict[l2_name]
                }
            )
            l3_loc = result['data']['rowId']
            loc_dict[l2_name + l3_name] = l3_loc
            
            
        #check if l4 location was already created; create it if not
        if l2_name + l3_name + l4_name not in loc_dict:      
            l4_type = l4_name.split(' ')[0]
            
            result = api.storage.create_storage_item(
                l4_type,
                {
                    'name': l4_name,
                    'locationId': loc_dict[l2_name + l3_name]
                }
            )
            l4_loc = result['data']['rowId']
            loc_dict[l2_name + l3_name + l4_name] = l4_loc
            
        #lookup terminal storage location types. these must be created in UI or separately via API because they're nuanced. 
        if box_name not in term_dict:
            term_type_id = api.query.select_rows(
                'inventory',
                'BoxType',
                filter_array=[
                    QueryFilter('Name', box_name, 'eq')
                    ],
                columns='RowId'
            )['rows'][0]['RowId']
            term_dict['box_name'] = term_type_id
        
        #create terminal storage
        api.storage.create_storage_item(
            'Terminal Storage Location',
            {
                'name': box,
                'typeId': term_dict['box_name'],
                'locationId': loc_dict[l2_name + l3_name + l4_name]
            }
        )
