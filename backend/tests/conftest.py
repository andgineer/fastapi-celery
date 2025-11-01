import logging
import os
from pathlib import Path

os.environ["CELERY_TRACK_STARTED"] = "True"
os.environ["CELERY_IGNORE_RESULT"] = "False"
os.environ["CELERY_TASK_RESULT_EXPIRES"] = "6000"

pytest_plugins = ("celery.contrib.pytest",)

# os.environ["ADMIN_LOGIN"] = "admin"
# os.environ["ADMIN_PASSWORD"] = "admin"
# os.environ["JWT_SECRET_KEY"] = "11d25e094faa6ca2556c818133b7a9563b93f7077f6f0f4caa6cf63b44e8d3e3"
# os.environ["AMQP_USERNAME"] = "guest"
# os.environ["AMQP_PASSWORD"] = "guest"
# os.environ["AMQP_HOST"] = "redis"
# os.environ["AMQP_PORT"] = "6379"

import app.config
import app.db.session
import pytest
import tests.config as test_config
from app import modules_load

app.config.get_config = test_config.get_test_config
app.db.session.get_session = test_config.get_test_session

# we have to import fixtures only after injecting test config
modules_load.asterisk(Path(__file__).parent / "fixtures", "tests.fixtures", globals())
from tests.fixtures.client import TestClientExternal  # just to remove warning

# - in fact it is already imported with `modules_load`

log = logging.getLogger()
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


def pytest_addoption(parser):
    """
    py.test options
    """
    parser.addoption(
        "--host",
        type=str,
        dest="host",
        help="""External server to test. Run tests for the host. Skips tests marked as unittests.""",
    )
    parser.addoption(
        "--header",
        type=str,
        nargs="*",
        dest="headers",
        help="""HTTP headers to add to all API requests.""",
    )


def pytest_report_header(config):
    host = config.getoption("host")
    if host is not None:
        host = TestClientExternal.url("")
    return f"{'>' * 5} {'unittests' if host is None else 'Testing server ' + host} {'<' * 5}\n"


def pytest_cmdline_main(config):
    """
    After command line is parsed
    """
    test_config._config = test_config.TestConfig(config=config)


def pytest_collection_modifyitems(config, items):
    if config.getoption("host"):
        # Skip un-relevant tests if we test external server (option `--host`)
        skip_unittests = pytest.mark.skip(
            reason="Skip tests for local code in server test mode (--host)",
        )
        skip_non_api = pytest.mark.skip(
            reason="Skip non API tests in server test mode (--host)",
        )
        for item in items:
            if "unittest" in item.keywords:
                item.add_marker(skip_unittests)
            if "client" not in item.fixturenames:
                item.add_marker(skip_non_api)

    else:  # if this is not external server test then add db fixture to prevent DB modifications by tests
        FIXTURES_TO_PROTECT_DB = ["client", "celery_app", "celery_worker"]
        for item in items:
            if (
                any(fixture in item.fixturenames for fixture in FIXTURES_TO_PROTECT_DB)
                and "does_not_change_db" not in item.keywords
            ):
                item.fixturenames.append("db")
