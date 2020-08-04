from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from functools import lru_cache
from app.config import Config


@lru_cache()
def engine(config: Config) -> Engine:
    return create_engine(
            config.db_uri,
            pool_pre_ping=True,
            pool_size=config.db_pool_size,
        )


def get_session(config: Config) -> Session:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine(config))()
