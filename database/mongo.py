import os
from dotenv import load_dotenv
import pymongo

from util.json_manager import serialize_models

load_dotenv()
connection = os.getenv("CONNECTION_STRING")
mongo_client = pymongo.MongoClient(connection)
db = mongo_client["Bachelor"]


## Helper method to get a specific collection from a database
## Add the database as parameter to access another database.
def get_collection(collection):
    return db.get_collection(collection)


def get_all_items_from_collection(collection):
    return list(serialize_models(collection.find({})))

def get_all_reviews_by_product_name(product_name):
    product = get_collection("products").find_one({"name": product_name})
    if product is None:
        return None
    return list(serialize_models(product["reviews"]))
    #return list(serialize_models(get_collection("products").find({"reviews": {"$exists": True}})))


def insert_to_collection(collection, item):
    # Add any item to a collection
    # Users, products, etc
    return collection.insert_one(item)

def get_single_item(collection, key, value):
    return serialize_models(collection.find_one({key: value
                                }))

## count_documents is not synchronous
def get_count_items(collection, key, value):
    return collection.count_documents({key: value})


def delete_from_collection(collection, item):
    # Delete any item to a collection
    # Users, products, etc
    return collection.delete_one(item)
