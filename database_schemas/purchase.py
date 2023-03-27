from mongoengine import DateTimeField, ObjectIdField, Document, ListField, EmbeddedDocument, FloatField, IntField, \
    EmbeddedDocumentField, StringField


class Purchase(EmbeddedDocument):
    product_id = ObjectIdField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)


class PurchaseDocument(Document):
    user_id = ObjectIdField(required=True)
    image_url = StringField(required=True)
    purchase_date = DateTimeField(required=True)
    items = ListField(EmbeddedDocumentField(Purchase))
