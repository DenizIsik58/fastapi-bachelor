import json
from bson import json_util


def serialize_models(created_item):
    return json.loads(json_util.dumps(created_item))
