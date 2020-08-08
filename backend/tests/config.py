"""
Injection functions to replace `get_config()` and `get_session()` in app under test
"""
from app.db.session import get_session
from sqlalchemy.orm import Session
from app.config import Config
from typing import Optional
import fakeredis


HTTP_TIMEOUT_SECONDS = 10


class TestConfig(Config):
    headers = None

    @property
    def celery_broker_uri(self):
        return 'memory://'

    @property
    def celery_backend_uri(self):
        return 'rpc://'

    @property
    def redis(self):
        return fakeredis.FakeStrictRedis()

    def __init__(self, config=None):
        if config is not None:  # init from pytest config
            # --host: server to test. if None we unittest with FASTAPI test client
            self.host = config.getoption('host')

            # --header: HTTP headers for all requests
            header_strings = config.getoption('headers')
            if header_strings is None:
                header_strings = {}
            self.headers = {}
            for option in header_strings:
                key, _, value = option.partition(':')
                self.headers[key] = value.strip()
        else:
            self.host = None
            self.headers = None
        super().__init__()


_config: Optional[Config] = None


def get_test_config():
    """
    test config injection - should replace `get_config()` in app under test
    """
    if _config is not None:
        return _config
    else:
        return TestConfig()


_session: Optional[Session] = None


def get_test_session(config: Config) -> Session:
    """
    Tests can inject session using `session`
    """
    if _session is not None:
        return _session
    else:
        return get_session(config)
