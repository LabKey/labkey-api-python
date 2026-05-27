#
# Copyright (c) 2020-2026 LabKey Corporation
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
from .container import ContainerWrapper
from .domain import DomainWrapper
from .experiment import ExperimentWrapper
from .query import QueryWrapper
from .security import SecurityWrapper
from .storage import StorageWrapper
from .server_context import ServerContext


class APIWrapper:
    """
    Wrapper for all of the supported API methods in the Python Client API. Makes it easier to use
    the supported API methods without having to manually pass around a ServerContext object.
    """

    def __init__(
        self,
        domain,
        container_path,
        context_path=None,
        use_ssl=True,
        verify_ssl=True,
        api_key=None,
        disable_csrf=False,
        allow_redirects=False,
    ):
        self.server_context = ServerContext(
            domain=domain,
            container_path=container_path,
            context_path=context_path,
            use_ssl=use_ssl,
            verify_ssl=verify_ssl,
            api_key=api_key,
            disable_csrf=disable_csrf,
            allow_redirects=allow_redirects,
        )
        self.container = ContainerWrapper(self.server_context)
        self.domain = DomainWrapper(self.server_context)
        self.experiment = ExperimentWrapper(self.server_context)
        self.query = QueryWrapper(self.server_context)
        self.security = SecurityWrapper(self.server_context)
        self.storage = StorageWrapper(self.server_context)
