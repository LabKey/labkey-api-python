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
from requests import exceptions


# base exception class for server responses
class RequestError(exceptions.HTTPError):
    default_msg = 'Server Error'

    def __init__(self, server_response=None):
        if server_response is not None:
            try:
                decoded = server_response.json()
                if 'exception' in decoded:
                    # use labkey server error message if available
                    msg = decoded['exception']
                    self.server_exception = decoded
                else:
                    msg = self.default_msg
            except ValueError:
                # no valid json to decode
                raise ServerNotFoundError(server_response)

            self.message = '{0}: {1}'.format(server_response.status_code, msg)

        self.response = server_response


class QueryNotFoundError(RequestError):
    default_msg = 'Query Resource Not Found'


class RequestAuthorizationError(RequestError):
    default_msg = 'Authorization Failed'


class ServerNotFoundError(RequestError):
    SERVER_NOT_FOUND_MSG = 'Server resource not found. Please verify context path and project path are valid'

    def __init__(self, server_response=None):
        self.message = '{0}: {1}'.format(server_response.status_code, self.SERVER_NOT_FOUND_MSG)
        self.response = server_response


class ServerContextError(exceptions.HTTPError):
    def __init__(self, inner_exception=None):
        self.message = self._get_message(inner_exception)
        self.exception = inner_exception

    def _get_message(self, e):
        switcher = {
            exceptions.SSLError:
                'Failed to match server SSL configuration. Ensure the server_context is configured correctly.'
        }
        return switcher.get(type(e), 'Please verify server_context is configured correctly')
