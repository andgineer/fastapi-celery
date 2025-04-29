from datetime import datetime, timedelta, timezone
from itertools import chain
from typing import Any, Dict

import app.config as app_config  # to not shadow global app var with FastAPI app
import jwt
from app.api.v1 import models as api_models
from app.api.v1.auth import router
from fastapi import Body, HTTPException


def authenticate_admin(login: str, password: str) -> bool:
    return (  # type: ignore
        login == app_config.get_config().admin_login
        and password == app_config.get_config().admin_password
    )


def create_access_token(
    payload: Dict[str, Any],
    expires_delta: timedelta = timedelta(minutes=15),
) -> str:
    """
    Create JWT
    """
    return jwt.encode(
        payload=dict(
            chain(
                payload.copy().items(),
                {"exp": datetime.now(timezone.utc) + expires_delta}.items(),
            ),
        ),
        key=app_config.get_config().jwt_secret_key,
        algorithm=app_config.get_config().jwt_algorithm,
    )


@router.post("", response_model=api_models.Token)  # type: ignore
def get_token(  # type: ignore
    credentials: api_models.Credentials = Body(
        None,
        description="User credentials",
        example={
            "login": "admin",
            "password": "admin",
        },
    ),
):
    """
    Return access token for the credentials.

    Current implementation returns token with `admin` scope for admin's login/password
    defined in env vars (see app.config).
    """
    if not authenticate_admin(login=credentials.login, password=credentials.password):
        raise HTTPException(status_code=400, detail="Incorrect user login or password")
    access_token = create_access_token(
        payload={"sub": "admin", "scopes": ["admin"]},
    )
    return {"token": access_token, "type": "bearer"}
