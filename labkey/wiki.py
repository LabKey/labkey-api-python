#
# Copyright (c) 2011-2015 LabKey Corporation
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

import os
import sys
import ssl
from functools import wraps
import json
import urllib2
import urllib
import pprint
import base64


def updateWiki(baseUrl, containerPath, wikiName, wikiBody, debug=False):
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
    readUrl = baseUrl.rstrip('/') +\
        "/wiki/" +\
        urllib2.quote(containerPath.strip('/')) +\
        "/editWiki.view?name=" +\
        wikiName
    
    #Get authenticated to send URL requests
    opener, aHeader =_create_post_opener()
    
    # Use the opener to fetch a URL request
    readRequest = urllib2.Request(readUrl,None,{"Authorization": aHeader })
    try:
        readResponse = opener.open(readRequest)
    except urllib2.HTTPError, e:
        print "There was a problem while attempting to submit the read the wiki page " + wikiName + " via the URL " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode())
        print "The HTTP client error was: "+ format(e)
        #print "The HTTP Response Headers are: \n" + str(e.info())
        #   print "The Response Body is \n" + str(e.read())
        return(1)
    data = readResponse.read()
    #print readResponse.info()
    #print readResponse.getcode()
    readResponse.close()


    # Search HTML response for required information on wiki. This is stored in the javascript 
    # variable named 
    #  - _wikiProps: for 14.3 and earlier
    #  - LABKEY._wiki.setProps for 15.1 and later
    dataList = data.split('\n')

    # If LabKey Server is v14.3 or earlier find line containing '_wikiProp'
    v = next((i for i in xrange(len(dataList)) if '_wikiProp' in dataList[i]), None)

    # If v = None, then server is running 15.1 or later and find the line  
    # containing 'LABKEY._wiki.setProps'
    if v == None: 
        v = next((i for i in xrange(len(dataList)) if 'LABKEY._wiki.setProps' in dataList[i]), None)

    # Verify that we found the variable in the HTML response. If not 
    # do not proceed
    if v == None: 
        print "There was a problem while attempting to submit the update the wiki page '" + wikiName + "'."
        print "The script is unable to find the wiki properties in the HTML response"
        return(1)

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
    updateUrl = baseUrl.rstrip('/') +\
        "/wiki/" +\
        urllib2.quote(containerPath.strip('/')) +\
        "/saveWiki.view?name=" +\
        wikiName
    
    # Update wikiVars to use the new wiki content. 
    wikiVars['body'] = wikiBody
    
    # Create the JSON needed to perform the update
    mypostdata = json.dumps(wikiVars)
    
    # Use the opener to fetch a URL request
    updateRequest = urllib2.Request(updateUrl, None, {'Content-Type': 'application/json', "Authorization": aHeader })
    try:
        UpdateResponse = opener.open(updateRequest, mypostdata)
        data = UpdateResponse.read()
        UpdateResponse.close()
        #print data        
    except urllib2.HTTPError, e:
        print "There was a problem while attempting to submit the update the wiki page " + wikiName + " via the URL " + e.geturl() + ". The HTTP response code was " + str(e.getcode())
        print "The HTTP client error was: "+ format(e)
        #print "The HTTP Response Headers are: \n" + e.info()
        #print "The Response Body is \n" + e.read()
        return(1)
    
    # Decode the JSON into a Python "dictionary" - an associative array
    data_dict = json.loads(data, object_hook=_decode_dict)
    return(data_dict)


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
