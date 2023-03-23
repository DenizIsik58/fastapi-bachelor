import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
connection = os.getenv("CONNECTION_STRING")
mongo_client = pymongo.MongoClient(connection)
db = mongo_client["Bachelor"]


## Helper method to get a specific collection from a database
def get_collection(collection):
    return db.get_collection(collection)


async def get_all_items_from_collection(collection):
    return list(collection.find({}))


def insert_to_collection(collection, item):
    print(item)
    # Add any item to a collection
    # Users, products, etc
    return collection.insert_one(item)


async def delete_from_collection(collection, item):
    # Delete any item to a collection
    # Users, products, etc
    return collection.delete_one(item)
