from bson import ObjectId
from mongoengine import *


class UserDocument(Document):
    username = StringField(required=True, max_length=50)
    email = StringField(required=True)
    salt = StringField(required=True)
    hashed_pwd = StringField(required=True)

