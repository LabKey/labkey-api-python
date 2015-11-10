#
# Copyright (c) 2011-2014 LabKey Corporation
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

import os
import sys
import ssl
from functools import wraps
import json
import urllib2
import urllib
import pprint
import base64


def postMessage(baseUrl, containerPath, messageTitle, messageBody, renderAs, debug=False):
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

The following are optional:

	debug = True	#will result in a more verbose output
	
The function will return the integer 0 for success and the integer 1 if the message post fails

----------------------------------------------------------------------------
Test Code:

[NOT AVAILABLE]

############################################################################
    """
    
    # Build the URL for querying LabKey Server      
    myurl = baseUrl.rstrip('/') +\
        "/announcements/" +\
        urllib2.quote(containerPath.strip('/')) +\
        "/insert.view?"
        
    mypostdata_unencoded = {\
        'title': messageTitle,
        'body': messageBody,
        'rendererType': renderAs}    
    mypostdata = urllib.urlencode(mypostdata_unencoded)
    
    #Get authenticated to send URL requests
    opener, aHeader =_create_post_opener()
    
    # Use the opener to fetch a URL request
    myrequest = urllib2.Request(myurl,None,{"Authorization": aHeader })
    try:
        response = opener.open(myrequest,mypostdata)
    except urllib2.HTTPError, e:
        print "There was problem while attempting to submit the message to " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode())
        print "The HTTP client error was: "+ format(e)
        #print "The HTTP Response Headers are: \n" + e.info()
        #print "The Response Body is \n" + e.read()
        return(0)
        
    return(1)


"""
############################################################################
############################################################################
Helper functions
############################################################################
"""
def sslwrap(func):
    """
    This is used to force the HTTPS requests to use TLSv1+ instead of 
    defaulting to SSLv3. Adapted from Stack Overflow:
        - http://stackoverflow.com/questions/9835506/urllib-urlopen-works-on-sslv3-urls-with-python-2-6-6-on-1-machine-but-not-wit/24158047#24158047
        - Thank you chnrxn
    """
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

def _print_debug_info(data_dict, myurl, mydata=None):
    """ Print the URL and any data used to query the server """
    print myurl
    if mydata: 
        print mydata
    
    # Review the results
    pp = pprint.PrettyPrinter(4)
    pp.pprint(data_dict)
    type(data_dict)
    
    # Look at the dictionary's keys
    mykeys = data_dict.keys()	
    print mykeys
    
    # Look at the list of rows
    rowlist = data_dict['rows']
    # Look at the first row of data
    if rowlist: 
        pp.pprint(rowlist[0])
        
    return

def _create_opener():	
    """
    Create an opener and load the login and password into the object. The
    opener will be used when connecting to the LabKey Server
    """
    # Check for credential file (which contains login and password for accessing
    # your LabKey Server) in either "LABKEY_CREDENTIALS" environment variable 
    # or in the file .labkeycredentials.txt in your home directory
    try: 
        credential_file_name = os.environ["LABKEY_CREDENTIALS"]
    except KeyError: 
        credential_file_name = os.environ["HOME"] + '/.labkeycredentials.txt'
    
    f = open(credential_file_name, 'r')
    mymachine = f.readline().strip().split(' ')[1]
    myusername = f.readline().strip().split(' ')[1]
    mypassword = f.readline().strip().split(' ')[1]
    f.close()

    # Force the opener to use TLSv1 or greater SSL Protocol for SSL connections
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    
    # Create a password manager
    passmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    
    # Add login info to the password manager
    passmanager.add_password(None, mymachine, myusername, mypassword)
    
    # Create the AuthHandler
    authhandler = urllib2.HTTPBasicAuthHandler(passmanager)
    
    # Create opener
    opener = urllib2.build_opener(authhandler)
    return opener

def _create_post_opener():	
    """ 
    Identical to _create_opener object accept this function will create the Basic Authentication 
    Header using the username and password in the credentials file and then will return both 
    the opener object and header string. 
    When submitting a POST, you will need to use this method. 
    """
    # Check for credential file (which contains login and password for accessing
    # your LabKey Server) in either "LABKEY_CREDENTIALS" environment variable 
    # or in the file .labkeycredentials.txt in your home directory
    try: 
        credential_file_name = os.environ["LABKEY_CREDENTIALS"]
    except KeyError: 
        credential_file_name = os.environ["HOME"] + '/.labkeycredentials.txt'
    
    f = open(credential_file_name, 'r')
    mymachine = f.readline().strip().split(' ')[1]
    myusername = f.readline().strip().split(' ')[1]
    mypassword = f.readline().strip().split(' ')[1]
    f.close()

    # Force the opener to use TLSv1 or greater SSL Protocol for SSL connections
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)

    # Create a password manager
    passmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add login info to the password manager
    passmanager.add_password(None, mymachine, myusername, mypassword)

    # Create the AuthHandler
    authhandler = urllib2.HTTPBasicAuthHandler(passmanager)
    
    # Create the Basic Authentication Header
    authHeader = base64.encodestring("%s:%s" % (myusername, mypassword))[:-1]
    authHeader = "Basic %s" % authHeader

    # Create opener
    opener = urllib2.build_opener(authhandler)
    return opener, authHeader

def _decode_list(lst):
    """
    Helper function for dealing with unicode
    Adapted from Stack Overflow: 
      http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-unicode-ones-from-json-in-python
      Answer from Mike Brennan: http://stackoverflow.com/users/658138/mike-brennan
      Question from Brutus: http://stackoverflow.com/users/11666/brutus
    """
    newlist = []
    for i in lst:
        if isinstance(i, unicode):
            i = i.encode('utf-8')
        elif isinstance(i, list):
            i = _decode_list(i)
        newlist.append(i)
    return newlist

def _decode_dict(dct):
    """
    Helper function for dealing with unicode
    Adapted from Stack Overflow: 
      http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-unicode-ones-from-json-in-python
      Answer from Mike Brennan: http://stackoverflow.com/users/658138/mike-brennan
      Question from Brutus: http://stackoverflow.com/users/11666/brutus
    """
    newdict = {}
    for k, v in dct.iteritems():
        if isinstance(k, unicode):
            k = k.encode('utf-8')
        if isinstance(v, unicode):
             v = v.encode('utf-8')
        elif isinstance(v, list):
            v = _decode_list(v)
        newdict[k] = v
    return newdict
