from pathlib import Path
import pytest
import app.config
import app.db.session
import logging

from app import modules_load
import config as test_config


app.config.get_config = test_config.get_test_config
app.db.session.get_session = test_config.get_test_session

# we have to import fixtures only after injecting test config
modules_load.asterisk(Path(__file__).parent / 'fixtures', 'fixtures', globals())
from fixtures.client import TestClientExternal  # just to remove warning
# - in fact it is already imported with `modules_load`

log = logging.getLogger()


def pytest_addoption(parser):
    """
    py.test options
    """
    parser.addoption(
        '--host',
        type='string',
        dest='host',
        help=f'''External server to test. Run tests for the host. Skips tests marked as unittests.''')
    parser.addoption(
        '--header',
        type='string',
        nargs='*',
        dest='headers',
        help=f'''HTTP headers to add to all API requests.''')


def pytest_report_header(config):
    host = config.getoption('host')
    if host is not None:
        host = TestClientExternal.url('')
    return (
        f'{">" * 5} ' 
        f'{"unittests" if host is None else "Testing server " + host} '
        f'{"<" * 5}\n'
    )


def pytest_cmdline_main(config):
    """
    After command line is parsed
    """
    test_config._config = test_config.TestConfig(config=config)


def pytest_collection_modifyitems(config, items):
    if config.getoption("host"):
        # Skip un-relevant tests if we test external server (option `--host`)
        skip_unittests = pytest.mark.skip(
            reason="Skip tests for local code in server test mode (--host)"
        )
        skip_non_api = pytest.mark.skip(
            reason="Skip non API tests in server test mode (--host)"
        )
        for item in items:
            if "unittest" in item.keywords:
                item.add_marker(skip_unittests)
            if 'client' not in item.fixturenames:
                item.add_marker(skip_non_api)

    else:  # if this is not external server test then add db fixture to prevent DB modifications by tests
        FIXTURES_TO_PROTECT_DB = ['client', 'celery_app', 'celery_worker']
        for item in items:
            if any(fixture in item.fixturenames for fixture in FIXTURES_TO_PROTECT_DB) \
                    and 'does_not_change_db' not in item.keywords:
                item.fixturenames.append('db')
