from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
import app.db.session as app_session
import pytest
import app.config as app_config
import logging
import uuid


log = logging.getLogger()


@pytest.fixture(
    scope='session',
)
def db(pytestconfig):
    """
    SQLAlchemy DB session from app.db.session.
    We need this fixture
        1) Simple and explicit way to get DB session in a test
        2) Raise exception if in External test mode we use unittests (with direct access to DB)
    """
    if app_config.get_config().host is not None:
        yield None
        # No sense using local DB when we in External server test mode.
        # We do not raise exception here because some tests can check External server test mode
        # by themselves and do not use the fixture in that mode. So this is ok if some
        # tests in External server test mode request but do not use the fixture.
    else:
        session = app_session.get_session(app_config.get_config())
        yield session
        session.close()


@pytest.fixture(
    scope='function',
)
def db_indepotent(pytestconfig):
    """
    DB session that roll back all DB modifications made in a test.
    So you do not need to write per-test tear-down for DB changes made by test.

    SQLAlchemy session for tests and for the code under tests started with SAVEPOINT.
    After test DB rollback to this SAVEPOINT.

    If we choose to use this approach the we better auto-add this fixture to all tests
    that use fixtures `client` and `celery_*` and is not marked as `does_not_change_db`.
    So to all tests that potentially could change DB in backend request handler or in Celery task.
    To do that uncomment the code inside `pytest_collection_modifyitems` hook.
    """
    if app_config.get_config().host is not None:
        yield None  # no sense using local DB when we test external Server
        return  # stop iterations for this fixture generator
    try:
        connection = app_session.engine(
            app_config.get_config()
        ).connect()
    except sqlalchemy.exc.OperationalError:
        pytest.exit(f'Tests have to connect to DB {app_config.get_config().db_uri}', returncode=2)

    # begin a non-ORM transaction
    trans = connection.begin()
    session = sessionmaker(info={'test_session_id': str(uuid.uuid4())})(bind=connection)

    session.begin_nested()  # SAVEPOINT
    log.debug(f'[[[ savepoint transaction ]]] Start in {session.info}')

    app_session._session = session  # Inject session to the server code under test
    # todo This session should not be used in parallel by backend handlers and Celery tasks.
    # todo So we have to implement custom session maker that wait for a mutex before giving
    # todo this session
    # todo And we should override `close` method in the DB session to release this mutex
    # todo but do not actually close the session so it will be given to next waiting handler/task.

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        """
        Each time that SAVEPOINT ends, reopen it
        """
        if transaction.nested and not transaction._parent.nested:
            log.debug(f'[[[ savepoint transaction ]]] Restart in {session.info}')
            session.begin_nested()

    yield session

    app_session._session = None  # remove so server code in future will generate session by itself
    session.close()
    log.debug(f'[[[ savepoint transaction ]]] Rollback in {session.info}')
    trans.rollback()  # roll back to the SAVEPOINT
    connection.close()
