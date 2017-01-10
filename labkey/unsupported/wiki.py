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
"""
WARNING: This module is not officially supported! Use at your own risk.

############################################################################
NAME: 
LabKey Collaboration API 

SUMMARY:  
This module provides functions for interacting with Wikis on LabKey Server.

DESCRIPTION:
This module is designed to simply programmatic editing of wikis on the LabKey Server

Documentation:
LabKey Python API:
https://www.labkey.org/wiki/home/Documentation/page.view?name=python

Setup, configuration of the LabKey Python API:
https://www.labkey.org/wiki/home/Documentation/page.view?name=setupPython

Using the LabKey Python API:
https://www.labkey.org/wiki/home/Documentation/page.view?name=usingPython

Documentation for the LabKey client APIs:
https://www.labkey.org/wiki/home/Documentation/page.view?name=viewAPIs

Support questions should be directed to the LabKey forum:
https://www.labkey.org/announcements/home/Server/Forum/list.view?

############################################################################
"""

import json
from labkey.utils import build_url, handle_response
import requests
from requests.exceptions import SSLError

def updateWiki(server_context, wikiName, wikiBody, container_path=None):
    """
############################################################################
updateWiki()

updateWiki() can be used to update an existing wiki page

The following are the minimum required params:

myresults = labkeyApi.updateWiki(
    baseUrl = 'https://hosted.labkey.com',
    containerPath = 'PythonProject',
    wikiName = 'MyWiki',
    wikiBody = 'New Content for my wiki')

The following are optional:

	debug = True	#will result in a more verbose output


This API does not support the ability to change the Render Type for the wiki to be updated. 

This API returns a dictionary containing the response from the server. The 'success' key
in the dictionary will be true when the wiki was successfully updated. It will be false 
in the case of a failure.  In the case of a failure, the 'error' key contains the error
message returned by the server. 

----------------------------------------------------------------------------
Test Code:

[NOT AVAILABLE]

############################################################################
"""
    
    # Build the URL for reading the wiki page
    read_wiki_url = build_url(server_context, 'wiki', 'editWiki.api', container_path=container_path)
    payload = {'name': wikiName}
    headers = {
        'Content-type': 'application/json'
    }

    data = None

    try:
        read_response = requests.get(read_wiki_url, params=payload, headers=headers) # editWiki action only takes URL parameters, not JSON (JSON is not bound to form)
    except SSLError as e:
        print("There was a problem while attempting to submit the read for the wiki page " + str(wikiName) + " via the URL " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode()))
        print("The HTTP client error was: "+ format(e))
        return(1) # TODO: this is incorrect, should return 'success'/'error' properly like the docs say

    data = read_response.text

    # Search HTML response for required information on wiki. This is stored in the javascript 
    # variable named 
    #  - _wikiProps: for 14.3 and earlier
    #  - LABKEY._wiki.setProps for 15.1 and later
    dataList = data.split('\n')

    # If LabKey Server is v14.3 or earlier find line containing '_wikiProp'
    v = next((i for i in range(len(dataList)) if '_wikiProp' in dataList[i]), None)

    # If v = None, then server is running 15.1 or later and find the line  
    # containing 'LABKEY._wiki.setProps'
    if v == None: 
        v = next((i for i in range(len(dataList)) if 'LABKEY._wiki.setProps' in dataList[i]), None)

    # Verify that we found the variable in the HTML response. If not 
    # do not proceed
    if v == None: 
        print("There was a problem while attempting to read the data for the wiki page '" + str(wikiName) + "'.")
        print("The script is unable to find the wiki properties in the HTML response")
        return(1) # TODO: this is incorrect, should return 'success'/'error' properly like the docs say

    wikiVars = {} 
    for j in range(100):
        # Read each line, until find a javascript closing bracket. 
        if '};' in dataList[v+j+1]:
            break
        if '});' in dataList[v+j+1]:
            break
        wvar = dataList[v+j+1].rstrip().lstrip().replace('\'','').replace(',','')
        wikiVars[wvar.split(':')[0]] = wvar.split(':')[1]
    
    # Build the URL for updating the wiki page
    update_wiki_url = build_url(server_context, 'wiki', 'saveWiki.api', container_path=container_path)
    headers = {
        'Content-type': 'application/json'
    }
    data = None

    # Update wikiVars to use the new wiki content.
    wikiVars['name'] = wikiName
    wikiVars['body'] = wikiBody

    try:
        response = requests.post(update_wiki_url, data=json.dumps(wikiVars, sort_keys=True), headers=headers)
        data = handle_response(response)
    except SSLError as e:
        print("There was a problem while attempting to submit the read for the wiki page '" + str(wikiName) + "' via the URL " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode()))
        print("The HTTP client error was: "+ format(e))
        return(1) # TODO: this is incorrect, should return 'success'/'error' properly like the docs say

    return(data)
