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
from __future__ import unicode_literals

import requests
import ssl

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from labkey.exceptions import RequestError, RequestAuthorizationError, QueryNotFoundError, ServerNotFoundError


# _ssl.c:504: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure
# http://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
class SafeTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def create_server_context(domain, container_path, context_path=None, use_ssl=True):
    """
    Create a LabKey server context. This context is used to encapsulate properties
    about the LabKey server that is being requested against. This includes, but is not limited to,
    the domain, container_path, and if the server is using SSL.
    :param domain:
    :param container_path:
    :param context_path:
    :param use_ssl:
    :return:
    """
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


def build_url(server_context, controller, action, container_path=None):
    """
    Builds a URL from a controller and an action. Users the server context to determine domain,
    context path, container, etc.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param controller: The controller to use in building the URL
    :param action: The action to use in building the URL
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

    if (200 <= sc < 300) or sc == 304:
        return response.json()
    elif sc == 401:
        raise RequestAuthorizationError(response)
    elif sc == 404:
        try:
            response.json()  # attempt to decode response
            raise QueryNotFoundError(response)
        except ValueError:
            # could not decode response
            raise ServerNotFoundError(response)
    else:
        raise RequestError(response)


