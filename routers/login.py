import json

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from base_models.login import BaseLogin
from base_models.settings import Settings
from base_models.token import Token
from util.authentication_manager import authenticate_and_verify_passwords
from util.json_manager import serialize_models

login_router = APIRouter()


@AuthJWT.load_config
def get_config():
    return Settings()


@login_router.post("/login", response_model=Token)
async def login_for_access_token(login_data: BaseLogin = Body(...), Authorize: AuthJWT = Depends()):
    is_authorized = authenticate_and_verify_passwords(login_data.username.lower(), login_data.password)

    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject=login_data.username.lower())
    refresh_token = Authorize.create_refresh_token(subject=login_data.username.lower())

    return JSONResponse(content=json.loads(Token(access_token=access_token, refresh_token=refresh_token).json()))
