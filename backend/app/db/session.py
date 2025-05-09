import logging
from typing import Any, Optional

from app.config import Config
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

_engine: Optional[Engine] = None  # cache
_session_maker: Any = None  # cache
_injected_session_maker: Any = None  # injection


log = logging.getLogger()


def engine(config: Config) -> Engine:
    global _engine  # pylint: disable=global-statement
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
    def receive_checkout(
        dbapi_connection: Any,  # pylint: disable=unused-argument
        connection_record: Any,  # pylint: disable=unused-argument
        connection_proxy: Any,  # pylint: disable=unused-argument
    ) -> None:
        nonlocal connections_checked_out_counter
        connections_checked_out_counter += 1
        log.debug(  # pylint: disable=logging-not-lazy
            "@" * 5 + f" DB connection checkOUT. Used: {connections_checked_out_counter}",
        )

    @event.listens_for(_engine, "checkin")
    def receive_checkin(
        dbapi_connection: Any,  # pylint: disable=unused-argument
        connection_record: Any,  # pylint: disable=unused-argument
    ) -> Any:
        nonlocal connections_checked_out_counter
        connections_checked_out_counter -= 1
        log.debug(  # pylint: disable=logging-not-lazy
            "@" * 5 + f" DB connection checkIN. Used: {connections_checked_out_counter}",
        )

    return _engine


def session_maker(config: Config) -> Any:
    global _session_maker  # pylint: disable=global-statement
    if not _session_maker:
        _session_maker = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine(config),
        )
    return _session_maker


def get_session(config: Config) -> Session:
    if _injected_session_maker is not None:
        return _injected_session_maker()  # type: ignore
    return session_maker(config)()  # type: ignore
