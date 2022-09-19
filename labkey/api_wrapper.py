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
    ):
        self.server_context = ServerContext(
            domain=domain,
            container_path=container_path,
            context_path=context_path,
            use_ssl=use_ssl,
            verify_ssl=verify_ssl,
            api_key=api_key,
            disable_csrf=disable_csrf,
        )
        self.container = ContainerWrapper(self.server_context)
        self.domain = DomainWrapper(self.server_context)
        self.experiment = ExperimentWrapper(self.server_context)
        self.query = QueryWrapper(self.server_context)
        self.security = SecurityWrapper(self.server_context)
        self.storage = StorageWrapper(self.server_context)
