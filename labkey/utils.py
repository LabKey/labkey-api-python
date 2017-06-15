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
from requests.exceptions import SSLError
from requests.packages.urllib3.poolmanager import PoolManager
from labkey.exceptions import RequestError, RequestAuthorizationError, QueryNotFoundError, \
    ServerContextError, ServerNotFoundError

__default_timeout = 60 * 5  # 5 minutes
CSRF_TOKEN = 'X-LABKEY-CSRF'
DISABLE_CSRF_CHECK = False  # Used by tests to disable CSRF token check


def create_server_context(domain, container_path, context_path=None, use_ssl=True, api_key=None):
    """
    Create a LabKey server context. This context is used to encapsulate properties
    about the LabKey server that is being requested against. This includes, but is not limited to,
    the domain, container_path, if the server is using SSL, and CSRF token request.
    :param domain:
    :param container_path:
    :param context_path:
    :param use_ssl:
    :param api_key:
    :return:
    """
    config = dict(domain=domain, container_path=container_path, context_path=context_path, use_ssl=use_ssl, api_key=api_key)

    return ServerContext(**config)


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
    return server_context.build_url(controller, action, container_path=container_path)


def handle_response(response):
    sc = response.status_code

    if (200 <= sc < 300) or sc == 304:
        try:
            return response.json()
        except ValueError:
            result = dict(
                status_code=sc,
                message="Request was successful but did not return valid json",
                content=response.content
            )
            return result

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


# _ssl.c:504: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure
# http://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
class SafeTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


class ServerContext(object):

    def __init__(self, **kwargs):
        self._container_path = kwargs.pop('container_path', None)
        self._context_path = kwargs.pop('context_path', None)
        self._domain = kwargs.pop('domain', None)
        self._use_ssl = kwargs.pop('use_ssl', True)
        self._api_key = kwargs.pop('api_key', None)

        self._session = requests.Session()

        if self._use_ssl:
            self._scheme = 'https://'
            self._session.mount(self._scheme, SafeTLSAdapter())
        else:
            self._scheme = 'http://'

    def build_url(self, controller, action, container_path=None):
        sep = '/'

        url = self._scheme + self._domain

        if self._context_path is not None:
            url += sep + self._context_path

        if container_path is not None:
            url += sep + container_path
        elif self._container_path is not None:
            url += sep + self._container_path

        url += sep + controller + '-' + action

        return url

    def make_request(self, url, payload, headers=None, timeout=300, method='POST'):

        if headers is None:
            if self._api_key is not None:
                headers = {
                    'apikey': self._api_key
                }
        else:
            if self._api_key is not None:
                headers['apikey'] = self._api_key

        if not DISABLE_CSRF_CHECK:
            global CSRF_TOKEN

            # CSRF check
            if CSRF_TOKEN not in self._session.headers.keys():
                try:
                    csrf_url = self.build_url('login', 'whoami.api')
                    response = handle_response(self._session.get(csrf_url))
                    self._session.headers.update({
                        CSRF_TOKEN: response['CSRF']
                    })
                except SSLError as e:
                    raise ServerContextError(e)

        try:
            if method is 'GET':
                raw_response = self._session.get(url, params=payload, headers=headers, timeout=timeout)
            else:
                raw_response = self._session.post(url, data=payload, headers=headers, timeout=timeout)
            return handle_response(raw_response)
        except SSLError as e:
            raise ServerContextError(e)
