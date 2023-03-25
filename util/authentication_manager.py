import bcrypt
from database_schemas.user import UserDocument


def get_user(username: str):
    user = UserDocument.objects(username=username).first()
    if user is None:
        return None
    return user


def authenticate_and_verify_passwords(username, password):
    user = get_user(username)
    if user is None:
        return False

    return bcrypt.checkpw(password.encode("utf-8"),
                          bcrypt.hashpw(password.encode("utf-8"), user["salt"].encode("utf-8")))
