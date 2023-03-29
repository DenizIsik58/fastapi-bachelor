import json
from bson import json_util
from collections.abc import Iterable


def to_json(item, *, singular=True):
    if not singular:
        return [json.loads(i.to_json()) | {'_id': str(i.id)} for i in item]

    return json.loads(item.to_json()) | {'_id': str(item.id)}


def serialize_models(created_item):
    return json.loads(json_util.dumps(created_item))
