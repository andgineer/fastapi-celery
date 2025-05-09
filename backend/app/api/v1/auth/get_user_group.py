from typing import Any, Dict, Optional, Tuple

import app.config as app_config  # to not shadow global app var with FastAPI app
import jwt
from app.api.v1 import models as api_models
from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import SecuritySchemeType
from fastapi.security import SecurityScopes
from fastapi.security.base import SecurityBase
from pydantic import BaseModel, Field, ValidationError


def extract_token(authorization_header_value: str) -> Tuple[str, str]:
    """
    Extract token value from HTTP header value ('Bearer <token_value>')
    """
    if not authorization_header_value:
        return "", ""
    scheme, _, token = authorization_header_value.partition(" ")
    return scheme, token


class JWTSchema(SecurityBase):
    type_ = Field(SecuritySchemeType.apiKey, alias="type")
    flows: BaseModel


class JwtPasswordBearer(SecurityBase):
    def __init__(
        self,
        tokenUrl: str,  # pylint: disable=unused-argument
        scopes: Dict[str, Any] | None = None,
    ):
        if not scopes:
            scopes = {}
        self.scopes = scopes
        self.model = JWTSchema()  # type: ignore
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")  # type: ignore
        scheme, param = extract_token(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return param


jwt_scheme = JwtPasswordBearer(
    tokenUrl="/api/auth",
    scopes={"admin": "Create/delete", "user": "Use"},
)


def get_user_group(
    security_scopes: SecurityScopes,
    token: str = Depends(jwt_scheme),
) -> str:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token,
            app_config.get_config().jwt_secret_key,
            algorithms=[app_config.get_config().jwt_algorithm],
        )
        user_group: str = payload.get("sub")
        if user_group is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = api_models.TokenData(scopes=token_scopes, user_group=user_group)
    except (jwt.PyJWTError, ValidationError) as e:
        raise credentials_exception from e
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user_group
