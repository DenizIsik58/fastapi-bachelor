from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from models.settings import Settings
from models.token import Token
from routers.register import oauth2_scheme
from util.authentication_manager import authenticate_and_verify_passwords

login_router = APIRouter()


@AuthJWT.load_config
def get_config():
    return Settings()


@login_router.post("", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
    is_authorized = authenticate_and_verify_passwords(form_data.username, form_data.password)
    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject=form_data.username)
    refresh_token = Authorize.create_refresh_token(subject=form_data.username)

    return JSONResponse({"access_token": access_token, "refresh_token": refresh_token})


# In case we need to fetch the user for protected endpoints
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = token
    return user
