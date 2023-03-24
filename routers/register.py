import bcrypt
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.responses import JSONResponse

from database.mongo import get_collection
from models.register import Register
from models.user import User
from util.json_manager import serialize_models

register_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@register_router.post("/")
async def register(form: Register = Body(...)):
    if not form.email.__contains__("@"):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")

    if form.password != form.password_repeat:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords does not match!")

    if get_collection("users").count_documents({"email": form.email}) > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists!")

    if get_collection("users").count_documents({"username": form.username}) > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is in use by someone else!")

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(form.password.encode("utf-8"), salt)

    user_obj = User(username=form.username, email=form.email, salt=salt, hashed_pwd=hashed_pwd)
    new_user = get_collection("users").insert_one(jsonable_encoder(user_obj))
    created_user = get_collection("users").find_one({"_id": new_user.inserted_id})
    user = {"email": created_user.get("email"), "username": created_user.get("username")}

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=serialize_models(user))
