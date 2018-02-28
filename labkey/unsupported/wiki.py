#
# Copyright (c) 2016-2017 LabKey Corporation
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
unsupported.wiki
~~~~~~~~~~~~~~~~
WARNING: This module is not officially supported! Use at your own risk.

This module provides functions for interacting with Wiki's on the
LabKey Server.
"""
from __future__ import unicode_literals

import json
from requests.exceptions import SSLError


def update_wiki(server_context, wiki_name, wiki_body, container_path=None):
    """
    Used to update an existing wiki page
    :param server_context: A LabKey server context. See labkey.utils.create_server_context.
    :param wiki_name: The name of the wiki.
    :param wiki_body: The body of the wiki.
    :param container_path: Optional container path that can be used to override the server_context container path
    :return: returns a dictionary containing the response from the server. The 'success' key
    in the dictionary will be true when the wiki was successfully updated. It will be false
    in the case of a failure.  In the case of a failure, the 'error' key contains the error
    message returned by the server.
    """
    # Build the URL for reading the wiki page
    read_wiki_url = server_context.build_url('wiki', 'editWiki.api', container_path=container_path)
    payload = {
        'name': wiki_name
    }
    headers = {
        'Content-type': 'application/json'
    }

    try:
        read_response = server_context.make_request(read_wiki_url, payload, headers=headers, method='GET',
                                                    non_json_response=True)
    except SSLError as e:
        print("There was a problem while attempting to submit the read for the wiki page " + str(wiki_name) + " via the URL " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode()))
        print("The HTTP client error was: " + format(e))
        return 1  # TODO: this is incorrect, should return 'success'/'error' properly like the docs say

    data = read_response.text

    # Search HTML response for required information on wiki. This is stored in the javascript 
    # variable named 
    #  - _wikiProps: for 14.3 and earlier
    #  - LABKEY._wiki.setProps for 15.1 and later
    data_list = data.split('\n')

    # If LabKey Server is v14.3 or earlier find line containing '_wikiProp'
    v = next((i for i in range(len(data_list)) if '_wikiProp' in data_list[i]), None)

    # If v = None, then server is running 15.1 or later and find the line  
    # containing 'LABKEY._wiki.setProps'
    if v is None: 
        v = next((i for i in range(len(data_list)) if 'LABKEY._wiki.setProps' in data_list[i]), None)

    # Verify that we found the variable in the HTML response. If not 
    # do not proceed
    if v is None: 
        print("There was a problem while attempting to read the data for the wiki page '" + str(wiki_name) + "'.")
        print("The script is unable to find the wiki properties in the HTML response")
        return 1  # TODO: this is incorrect, should return 'success'/'error' properly like the docs say

    wiki_vars = {} 
    for j in range(100):
        # Read each line, until find a javascript closing bracket. 
        if '};' in data_list[v+j+1]:
            break
        if '});' in data_list[v+j+1]:
            break
        wvar = data_list[v+j+1].rstrip().lstrip().replace('\'', '').replace(',', '')
        wiki_vars[wvar.split(':')[0]] = wvar.split(':')[1]
    
    # Build the URL for updating the wiki page
    update_wiki_url = server_context.build_url('wiki', 'saveWiki.api', container_path=container_path)
    headers = {
        'Content-type': 'application/json'
    }

    # Update wiki_vars to use the new wiki content.
    wiki_vars['name'] = wiki_name
    wiki_vars['body'] = wiki_body

    try:
        data = server_context.make_request(update_wiki_url, payload=json.dumps(wiki_vars, sort_keys=True),
                                           headers=headers, non_json_response=True)
    except SSLError as e:
        print("There was a problem while attempting to submit the read for the wiki page '" + str(wiki_name) + "' via the URL " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode()))
        print("The HTTP client error was: " + format(e))
        return 1  # TODO: this is incorrect, should return 'success'/'error' properly like the docs say

    return data
