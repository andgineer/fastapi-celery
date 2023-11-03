import logging
import os
from functools import lru_cache

import redis

API_V1_STR = "/api"


@lru_cache()
def get_config() -> "Config":
    return Config()


log = logging.getLogger()


DB_HOST_DEFAUL = "postgres"
DB_POOL_SIZE_DEFAUL = 10
DB_DATABASE_DEFAULT = "postgres"
DB_USER_DEFAULT = "postgres"
DB_PASSWORD_DEFAULT = "postgres"


class EnvironmentVarNames:
    """OS environment vars with configuration."""

    admin_login = "ADMIN_LOGIN"  # login to get admin JWT
    admin_password = "ADMIN_PASSWORD"  # password to get admin JWT
    jwt_secret_key = "JWT_SECRET_KEY"  # string to generate SECRET key

    db_host = "POSTGRES_HOST"
    db_database = "POSTGRES_DB"
    db_user = "POSTGRES_USER"
    db_password = "POSTGRES_PASSWORD"
    db_pool_size = "DB_POOL_SIZE"

    mq_user = "AMQP_USERNAME"
    mq_password = "AMQP_PASSWORD"
    mq_host = "AMQP_HOST"
    mq_port = "AMQP_PORT"


class Config:
    """Create the object with proper env and then get fastapi `app` or `celery_app`."""

    print(f"LOGIN: {os.getenv(EnvironmentVarNames.admin_login)}")
    # todo separate config for celery worker - it does not need admin password for example
    admin_login: str = os.getenv(EnvironmentVarNames.admin_login, None)
    admin_password: str = os.getenv(EnvironmentVarNames.admin_password, None)
    jwt_secret_key: str = os.getenv(EnvironmentVarNames.jwt_secret_key, None)
    if not admin_login or not admin_password or not jwt_secret_key:
        raise Exception(
            f'\n\n{"!"*110}\n'
            f"(!) Please specify admin login (got {admin_login})"
            f" / password (got {admin_password})"
            f" and JWT secret key (got {jwt_secret_key})"
            f"\nin env vars "
            f"{EnvironmentVarNames.admin_login} / {EnvironmentVarNames.admin_password}, "
            f"{EnvironmentVarNames.jwt_secret_key} (!)\n"
            f'{"!" * 110}\n\n'
        )
    jwt_algorithm = "HS256"

    db_database: str = os.getenv(EnvironmentVarNames.db_database, DB_DATABASE_DEFAULT)
    db_user: str = os.getenv(EnvironmentVarNames.db_user, DB_USER_DEFAULT)
    db_password: str = os.getenv(EnvironmentVarNames.db_password, DB_PASSWORD_DEFAULT)
    db_host: str = os.getenv(EnvironmentVarNames.db_host, DB_HOST_DEFAUL)
    db_pool_size: int = os.getenv(EnvironmentVarNames.db_pool_size, DB_POOL_SIZE_DEFAUL)

    mq_user = os.environ[EnvironmentVarNames.mq_user]
    mq_password = os.environ[EnvironmentVarNames.mq_password]
    mq_host = os.environ[EnvironmentVarNames.mq_host]
    mq_port = os.environ[EnvironmentVarNames.mq_port]

    def __init__(self) -> None:
        log.info(f'<<<Backend started with MQ "{self.mq_uri}" and DB "{self.db_uri}">>>')

    @property
    def db_uri(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}@"
            f"{self.db_host}/{self.db_database}"
        )

    @property
    def mq_uri(self) -> str:
        return f"pyamqp://{self.mq_user}:{self.mq_password}@{self.mq_host}:{self.mq_port}/"

    @property
    def redis_host(self) -> str:
        return self.mq_host

    @property
    def redis_port(self) -> int:
        return int(self.mq_port)

    @property
    def redis_db(self) -> int:
        return 1

    @property
    def redis(self) -> redis.Redis:
        return redis.Redis(  # type: ignore
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
            db=self.redis_db,
        )

    @property
    def redis_password(self) -> str:
        return self.mq_password

    @property
    def celery_broker_uri(self) -> str:
        return f"redis://:{self.mq_password}@{self.mq_host}:{self.mq_port}/0"

    @property
    def celery_backend_uri(self) -> str:
        return self.celery_broker_uri
