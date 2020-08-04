from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from app.db.session import engine
import pytest
import config
import logging
import uuid


log = logging.getLogger()


@pytest.fixture(
    scope='function',
)
def db(pytestconfig):
    """
    SQLAlchemy session for tests and for the code under tests started with SAVEPOINT.
    After test rollback to this SAVEPOINT.

    We auto-add this fixture to all tests that use fixtures `client`, `celery_app` and `celery_worker
    but is not marked as `does_not_change_db` - see `pytest_collection_modifyitems` hook

    And tests that do something directly in DB can use this fixture implicitly
    """
    try:
        connection = engine(
            config.get_test_config()
        ).connect()
    except sqlalchemy.exc.OperationalError:
        pytest.exit(f'Tests have to connect to DB {config.get_test_config().db_uri}', returncode=2)

    # begin a non-ORM transaction
    trans = connection.begin()
    session = sessionmaker(info={'test_session_id': str(uuid.uuid4())})(bind=connection)

    session.begin_nested()  # SAVEPOINT
    log.debug(f'[[[ savepoint transaction ]]] Start in {session.info}')

    config._session = session  # Inject session to the server code under test

    @event.listens_for(config._session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        """
        Each time that SAVEPOINT ends, reopen it
        """
        if transaction.nested and not transaction._parent.nested:
            log.debug(f'[[[ savepoint transaction ]]] Restart in {session.info}')
            session.begin_nested()

    yield session

    config._session = None  # remove so server code in future will generate session by itself
    session.close()
    log.debug(f'[[[ savepoint transaction ]]] Rollback in {session.info}')
    trans.rollback()  # roll back to the SAVEPOINT
    connection.close()
