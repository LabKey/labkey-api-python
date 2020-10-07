import requests
from requests.exceptions import RequestException
from labkey.exceptions import (
    RequestError,
    RequestAuthorizationError,
    QueryNotFoundError,
    ServerContextError,
    ServerNotFoundError,
)

API_KEY_TOKEN = "apikey"
CSRF_TOKEN = "X-LABKEY-CSRF"


def handle_response(response, non_json_response=False):
    sc = response.status_code

    if (200 <= sc < 300) or sc == 304:
        try:
            if non_json_response:
                return response
            return response.json()
        except ValueError:
            result = dict(
                status_code=sc,
                message="Request was successful but did not return valid json",
                content=response.content,
            )
            return result

    elif sc == 401:
        raise RequestAuthorizationError(response)
    elif sc == 404:
        try:
            if non_json_response:
                return response
            response.json()  # attempt to decode response
            raise QueryNotFoundError(response)
        except ValueError:
            # could not decode response
            raise ServerNotFoundError(response)
    else:
        # consider response.raise_for_status()
        raise RequestError(response)


class ServerContext:
    """
    ServerContext is used to encapsulate properties about the LabKey server that is being requested
    against. This includes, but is not limited to, the domain, container_path, if the server is
    using SSL, and CSRF token request.
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
        self._container_path = container_path
        self._context_path = context_path
        self._domain = domain
        self._use_ssl = use_ssl
        self._verify_ssl = verify_ssl
        self._api_key = api_key
        self._disable_csrf = disable_csrf
        self._session = requests.Session()

        if self._use_ssl:
            self._scheme = "https://"
            if not self._verify_ssl:
                self._session.verify = False
        else:
            self._scheme = "http://"

    def __repr__(self):
        return f"<ServerContext [ {self._domain} | {self._context_path} | {self._container_path} ]>"

    def build_url(self, controller: str, action: str, container_path: str = None) -> str:
        sep = "/"

        url = self._scheme + self._domain

        if self._context_path is not None:
            url += sep + self._context_path

        if container_path is not None:
            url += sep + container_path
        elif self._container_path is not None:
            url += sep + self._container_path

        url += sep + controller + "-" + action

        return url

    def handle_request_exception(self, exception):
        if type(exception) in [RequestAuthorizationError, QueryNotFoundError, ServerNotFoundError]:
            raise exception

        raise ServerContextError(self, exception)

    def make_request(
        self,
        url: str,
        payload: any,
        headers: dict = None,
        timeout: int = 300,
        method: str = "POST",
        non_json_response: bool = False,
        file_payload: any = None,
    ) -> any:
        if self._api_key is not None:
            if self._session.headers.get(API_KEY_TOKEN) is not self._api_key:
                self._session.headers.update({API_KEY_TOKEN: self._api_key})

        if not self._disable_csrf:
            if CSRF_TOKEN not in self._session.headers.keys():
                try:
                    csrf_url = self.build_url("login", "whoami.api")
                    response = handle_response(self._session.get(csrf_url))
                    self._session.headers.update({CSRF_TOKEN: response["CSRF"]})
                except RequestException as e:
                    self.handle_request_exception(e)

        try:
            if method == "GET":
                raw_response = self._session.get(
                    url, params=payload, headers=headers, timeout=timeout
                )
            else:
                if file_payload is not None:
                    raw_response = self._session.post(
                        url,
                        data=payload,
                        files=file_payload,
                        headers=headers,
                        timeout=timeout,
                    )
                else:
                    raw_response = self._session.post(
                        url, data=payload, headers=headers, timeout=timeout
                    )
            return handle_response(raw_response, non_json_response)
        except RequestException as e:
            self.handle_request_exception(e)
