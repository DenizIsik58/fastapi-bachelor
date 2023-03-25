from bson import ObjectId
from mongoengine import StringField, Document, ListField, EmbeddedDocumentField, FloatField
from database_schemas.review import ReviewDocument

"""
Consider using a reference field instead of an embedded document field
MongoDb has a limit of 16mb per document, so if you have a lot of reviews, this might be a problem
"""


class ProductDocument(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
