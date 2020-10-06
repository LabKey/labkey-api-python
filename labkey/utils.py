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
import json
from functools import wraps
from datetime import date, datetime

from .server_context import ServerContext


def create_server_context(
    domain: str,
    container_path: str,
    context_path: str = None,
    use_ssl: bool = True,
    verify_ssl: bool = True,
    api_key: str = None,
    disable_csrf: bool = False,
) -> ServerContext:
    """
    Create a LabKey server context. This context is used to encapsulate properties
    about the LabKey server that is being requested against. This includes, but is not limited to,
    the domain, container_path, if the server is using SSL, and CSRF token request.
    :param domain:
    :param container_path:
    :param context_path:
    :param use_ssl:
    :param verify_ssl:
    :param api_key:
    :param disable_csrf:
    :return:
    """
    return ServerContext(
        domain=domain,
        container_path=container_path,
        context_path=context_path,
        use_ssl=use_ssl,
        verify_ssl=verify_ssl,
        api_key=api_key,
        disable_csrf=disable_csrf,
    )


# Issue #14: json.dumps on datetime throws TypeError
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        return super(DateTimeEncoder, self).default(o)


@wraps(json.dumps)
def json_dumps(*args, **kwargs):
    kwargs.setdefault("cls", DateTimeEncoder)
    return json.dumps(*args, **kwargs)
