"""
Injection functions to replace `get_config()` and `get_session()` in app under test
"""
from typing import Optional

import fakeredis
from app.config import Config
from app.db.session import get_session
from sqlalchemy.orm import Session

HTTP_TIMEOUT_SECONDS = 10
_config: Optional[Config] = None  # Inject test config here
_session: Optional[Session] = None  # Inject test session here


class TestConfig(Config):
    headers = None

    @property
    def celery_broker_uri(self):
        return "memory://localhost//"

    @property
    def celery_backend_uri(self):
        return "cache+memory://"

    @property
    def redis(self):
        return fakeredis.FakeStrictRedis()

    def __init__(self, config=None):
        if config is not None:  # init from pytest config
            # --host: server to test. if None we unittest with FASTAPI test client
            self.host = config.getoption("host")

            # --header: HTTP headers for all requests
            header_strings = config.getoption("headers")
            if header_strings is None:
                header_strings = {}
            self.headers = {}
            for option in header_strings:
                key, _, value = option.partition(":")
                self.headers[key] = value.strip()
        else:
            self.host = None
            self.headers = None
        super().__init__()


def get_test_config():
    """Test config injection from `_config`."""
    return _config if _config is not None else TestConfig()


def get_test_session(config: Config) -> Session:
    """Test session injection from `_session`."""
    return _session if _session is not None else get_session(config)
