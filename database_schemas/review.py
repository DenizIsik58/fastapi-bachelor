from mongoengine import StringField, EmbeddedDocument, IntField, DateTimeField

"""
Consider using a reference field instead of an embedded document field
MongoDb has a limit of 16mb per document, so if you have a lot of reviews, this might be a problem
"""


class ReviewDocument(EmbeddedDocument):
    comment = StringField(required=True)
    product_name = StringField(required=True)
    rating = IntField(required=True)
    rater = StringField(required=True)
    timestamp = DateTimeField(required=True)

