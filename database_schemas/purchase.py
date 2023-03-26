from mongoengine import DateTimeField, ObjectIdField, Document, ListField, EmbeddedDocument, FloatField, IntField


class Purchase(EmbeddedDocument):
    product_id = ObjectIdField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    total = FloatField(required=True)
    date = DateTimeField(required=True)


class PurchaseDocuments(Document):
    user_id = ObjectIdField(required=True)
    purchases = ListField(Purchase)
