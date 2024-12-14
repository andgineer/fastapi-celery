import logging
from typing import Optional

from app.config import Config
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

_engine: Optional[Engine] = None  # cache
_session_maker: Optional[sessionmaker] = None  # cache
_injected_session_maker: Optional[sessionmaker] = None  # injection


log = logging.getLogger()


def engine(config: Config) -> Engine:
    global _engine
    if _engine:
        return _engine

    _engine = create_engine(
        config.db_uri,
        pool_pre_ping=True,
        pool_size=config.db_pool_size,
    )

    # event listeners to visualize potential connection pool leakage
    connections_checked_out_counter = 0

    @event.listens_for(_engine, "checkout")
    def receive_checkout(dbapi_connection, connection_record, connection_proxy):
        nonlocal connections_checked_out_counter
        connections_checked_out_counter += 1
        log.debug(
            "@" * 5
            + f" DB connection checkOUT. Used: {connections_checked_out_counter}"
        )

    @event.listens_for(_engine, "checkin")
    def receive_checkin(dbapi_connection, connection_record):
        nonlocal connections_checked_out_counter
        connections_checked_out_counter -= 1
        log.debug(
            "@" * 5 + f" DB connection checkIN. Used: {connections_checked_out_counter}"
        )

    return _engine


def session_maker(config: Config) -> sessionmaker:
    global _session_maker
    if not _session_maker:
        _session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=engine(config)
        )
    return _session_maker


def get_session(config: Config) -> Session:
    if _injected_session_maker is not None:
        return _injected_session_maker()
    else:
        return session_maker(config)()
