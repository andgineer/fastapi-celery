"""
HTTP clients for API testing
"""
import logging
from pprint import pformat
from pprint import pprint
from urllib.parse import urljoin

import app.main
import tests.config as config
import pytest
import requests
from starlette.testclient import TestClient

log = logging.getLogger()


class TestClientExternal(requests.Session):
    """
    Replacement for TestClient to test external server
    """

    @staticmethod
    def url(relative_url):
        if config.get_test_config().host.startswith("http"):
            return urljoin(config.get_test_config().host, relative_url)
        else:
            return urljoin(f"http://{config.get_test_config().host}", relative_url)

    def _proxy_method(self, method):
        """
        Proxy HTTP method to requests lib
        We add base URL from cmd line and we do not allow redirects so we can test 303 answer
        """

        def proxy(relative_url, **kwargs):
            return getattr(self, "__" + method)(
                self.url(relative_url),
                allow_redirects=False,
                verify=False,
                timeout=config.HTTP_TIMEOUT_SECONDS,
                **kwargs,
            )

        return proxy

    def __init__(self):
        super().__init__()
        for method in ("post", "get", "delete"):
            setattr(self, "__" + method, getattr(self, method))
            setattr(self, method, self._proxy_method(method))


class TextClientTooling:
    """
    Mixin for TestClient with test helpers like extended logging and JWT support.

    Should be the first in parents lists so it will override `request`.

    If you add `__init__` you have to call `TestClient.__init__(app)` in it so we will init.
    """

    def request(self, method, url, **args):
        args["headers"] = config.get_test_config().headers.copy()
        if "token" in args:
            args["headers"]["Authorization"] = f'Bearer {args["token"]}'
            del args["token"]
        result = super().request(method, url, **args)
        ellipsed_headers = {}
        MAX_LEN = 15
        for header, val in args["headers"].items():
            ellipsed_headers[header] = (
                val[:MAX_LEN] + ".." if len(val) > MAX_LEN else val
            )
        print()
        print("->>", method.upper(), url)
        log.info(f"->> {method.upper()} {url}")
        if ellipsed_headers:
            print("    HTTP headers:", pformat(ellipsed_headers))
            log.info(f"    HTTP headers: {pformat(ellipsed_headers)}")
        if "params" in args:
            print("Query params:", args["params"])
            log.info(f'Query params: {args["params"]}')
        if "json" in args:
            print("Request body:", args["json"])
            log.info(f'Request body: {args["json"]}')
        print("<<-", result.status_code)
        log.info(f"<<- {result.status_code}")
        try:
            pprint(result.json())
            log.info(pformat(result.json()))
        except Exception:
            print(result.text)
            log.info(result.text)
        return result


class TextClientExtWithTools(TextClientTooling, TestClientExternal):
    pass


class TextClientWithTools(TextClientTooling, TestClient):
    pass


@pytest.fixture(scope="function")
def client():
    """
    Client to call API from tests.
    Use FASTAPI TestClient to test local server code without actual HTTP connection.
    If `--host` use `requests` for real HTTP requests.
    """
    if config.get_test_config().host is None:
        return TextClientWithTools(app.main.app)
    else:
        return TextClientExtWithTools()
