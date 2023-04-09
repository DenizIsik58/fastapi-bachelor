import json
from bson import json_util
from collections.abc import Iterable


def to_json(item, *, singular=True):
    if not singular:
        return [json.loads(i.to_json()) | {'_id': str(i.id)} for i in item]

    return json.loads(item.to_json()) | {'_id': str(item.id)}


def to_json_purchases(item, *, singular=True):

    if not singular:
        return [json.loads(i.to_json()) | {'_id': str(i.id)} | {'purchase_date': str(i.purchase_date)} |
                {'items': [json.loads(product.to_json()) | {'product_id': str(product.product_id)} for product in
                           item[0]['items']]} for i in item]

    return json.loads(item.to_json()) | {'_id': str(item.id)} | {'purchase_date': str(item.purchase_date)} | {'items': [json.loads(product.to_json()) | {'product_id': str(product.product_id)} for product in
                           item['items']]}

def to_json_reviews(item, *, singular=True):
    if not singular:
        return [json.loads(i.to_json()) | {'_id': str(i.id)} | {'timestamp': str(i.timestamp)} for i in item]

    return json.loads(item.to_json()) | {'_id': str(item.id)} | {'timestamp': str(item.timestamp)}


def serialize_models(created_item):
    return json.loads(json_util.dumps(created_item))
