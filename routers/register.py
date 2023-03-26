import json

import bcrypt
from fastapi import APIRouter, Body, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.responses import JSONResponse

from base_models.register import Register
from database_schemas.user import UserDocument

register_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@register_router.post("/")
async def register(form: Register = Body(...)):
    if not form.email.__contains__("@"):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")

    if form.password != form.password_repeat:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords do not match!")

    if UserDocument.objects(email=form.email).count() > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists!")

    if UserDocument.objects(username=form.username).count() > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is in use by someone else!")

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(form.password.encode("utf-8"), salt)

    new_user = UserDocument(username=form.username, email=form.email, salt=salt, hashed_pwd=hashed_pwd).save()
    # TODO: Don't query the id again
    created_user = UserDocument.objects(id=new_user.id).exclude("salt", "hashed_pwd").to_json()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(created_user))
