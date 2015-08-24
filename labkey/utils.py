#
# Copyright (c) 2015 LabKey Corporation
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
from __future__ import unicode_literals

import requests
import ssl

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


# _ssl.c:504: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure
# http://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
class SafeTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def create_server_context(domain, container_path, context_path=None, use_ssl=True):
    # TODO: Document
    server_context = dict(domain=domain, container_path=container_path, context_path=context_path)

    if use_ssl:
        scheme = 'https'
    else:
        scheme = 'http'
    scheme += '://'

    if use_ssl:
        session = requests.Session()
        session.mount(scheme, SafeTLSAdapter())
    else:
        # TODO: Is there a better way? Can we have session.mount('http')?
        session = requests

    server_context['scheme'] = scheme
    server_context['session'] = session

    return server_context


def build_url(controller, action, server_context, container_path=None):
    """
    Builds a URL from a controller and an action. Users the server context to determine domain,
    context path, container, etc.
    :param controller: The controller to use in building the URL
    :param action: The action to use in building the URL
    :param server_context:
    :param container_path:
    :return:
    """
    sep = '/'

    url = server_context['scheme']
    url += server_context['domain']

    if server_context['context_path'] is not None:
        url += sep + server_context['context_path']

    url += sep + controller

    if container_path is not None:
        url += sep + container_path
    else:
        url += sep + server_context['container_path']

    url += sep + action

    return url


def handle_response(response):
    sc = response.status_code

    if sc == 200 or sc == 207:
        return response.json()
    elif sc == 401:
        print(str(sc) + ": Authorization failed.")
    elif sc == 404:
        msg = str(sc) + ": "
        decoded = response.json()
        if 'exception' in decoded:
            msg += decoded['exception']
        else:
            msg += 'Not found.'
        print(msg)
    elif sc == 500:
        msg = str(sc) + ": "
        decoded = response.json()
        if 'exception' in decoded:
            msg += decoded['exception']
        else:
            msg += 'Internal Server Error.'
        print(msg)
    else:
        print(str(sc))
        print(response.json())

    return None
