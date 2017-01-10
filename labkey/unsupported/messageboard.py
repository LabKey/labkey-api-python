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
LabKey Message Board API 

SUMMARY:  
This module provides functions for interacting with Message Boards on the
LabKey Server.

DESCRIPTION:
This module is designed to simply programmatic editing of wikis and posting messages 
to Message Boards/Forums on the LabKey Server

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

from labkey.utils import build_url, handle_response
import requests
from requests.exceptions import SSLError


def postMessage(server_context, messageTitle, messageBody, renderAs, container_path=None):
    """
############################################################################
postMessage()

postMessage() can be used to post a message to a message board on the LabKey Server

The following are the minimum required params:

myresults = labkeyApi.postMessage(
    baseUrl = 'https://hosted.labkey.com',
    containerPath = 'PythonProject',
    messageTitle = 'Message Title',
    messageBody = 'This is the content of my message ....', 
    renderAs = 'HTML')
	
The function will return the integer 1 for success and the integer 0 if the message post fails

----------------------------------------------------------------------------
Test Code:

[NOT AVAILABLE]

############################################################################
    """
    
    # Build the URL for querying LabKey Server
    message_url = build_url(server_context, 'announcements', 'insert.api', container_path=container_path)

    message_data = {
        'title': messageTitle,
        'body': messageBody,
        'rendererType': renderAs
    }

    session = server_context['session']
    data = None

    try:
        message_response = requests.post(message_url, message_data, headers=None)  # seems to be happy with Python dict directly
    except SSLError as e:
        print("There was problem while attempting to submit the message to " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode()))
        print("The HTTP client error was: "+ format(e))
        return(0)
        
    return(1)
