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
from requests import exceptions, Response


# base exception class for server responses
class RequestError(exceptions.RequestException):
    default_msg = "Server Error"

    def __init__(self, server_response, **kwargs):
        """
        :type server_response: Response
        """
        super().__init__(**kwargs)

        # base class allows for kwargs 'request' and 'response'
        self.response = server_response
        self.server_exception = None

        if self.response is not None:
            msg = self.default_msg
            try:
                decoded = self.response.json()
                if "exception" in decoded:
                    # use labkey server error message if available
                    msg = decoded["exception"]
                    self.server_exception = decoded
            except ValueError:
                # no valid json to decode
                pass

            self.message = "{0}: {1}".format(self.response.status_code, msg)
        else:
            self.message = "No response received"

    def __str__(self):
        return repr(self.message)


class QueryNotFoundError(RequestError):
    default_msg = "Query Resource Not Found"


class RequestAuthorizationError(RequestError):
    default_msg = "Authorization Failed"


class ServerNotFoundError(RequestError):
    default_msg = "Server resource not found. Please verify context path and project path are valid"


class ServerContextError(RequestError):
    def __init__(self, server_context, inner_exception):
        self.message = self._get_message(server_context, inner_exception)
        self.exception = inner_exception

    @staticmethod
    def _get_message(server_context, e):
        switcher = {
            exceptions.ConnectionError: "Failed to connect to server. Ensure the server_context domain, context_path, "
            "and SSL are configured correctly.",
            exceptions.InvalidURL: "Failed to parse URL. Context is " + str(server_context),
            exceptions.SSLError: "Failed to match server SSL configuration. Ensure the server_context is configured correctly.",
        }
        # #12 Pass through the exception message if available
        return switcher.get(
            type(e),
            str(e) if str(e) else "Please verify server_context is configured correctly.",
        )
