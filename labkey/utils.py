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


def transform_helper(userTransformFunc, filePathRunProperties):
    #filePathRunProperties must be explicitly defined as ${runInfo} within the user's transform script
    #parse run properties to for results data in and out filepaths
    filePathIn = ''
    filePathOut = ''
    fileRunProperties = open(filePathRunProperties) 
    for l in fileRunProperties:
        row = l.strip().split('\t')
        if row[0] == 'runDataFile':
            filePathIn = row[1]
            filePathOut = row[3]
    fileRunProperties.close()
    
    #parse results data into array, confirming supported file type is used
    fileIn = open(filePathIn)
    dataGrid = []
    
    for l in fileIn:
        if '\t' in l:
            row = l.replace('\n', '').split('\t')
        elif ',' in l:
            row = l.replace('\n', '').split(',')
        else:
            raise ValueError('Unsupported file type or delimiter used. Header used: \n' + str(l))
        dataGrid.append(row)    
    fileIn.close()
    
    #run user transform on parsed results data array
    transformedGrid = userTransformFunc(dataGrid)
    
    #write transformed results data array to LabKey assay results data grid
    #transformed array must be a python list object, not a numpy array or pandas dataframe
    fileOut = open(filePathOut, mode='w')
    for row in transformedGrid:
        row = [str(el).strip() for el in row]
        row = '\t'.join(row)        
        fileOut.write(row + '\n')
    
    fileOut.close()
