import json

import requests

from database_schemas.product import ProductDocument


def load_products_to_db():
    with open("products.json", "r") as f:
        products = json.load(f)

        for product in products:
            if ProductDocument.objects(name=product["name"]).count() > 0:
                print("This bag already exists!")
                continue
            requests.post("http://172.105.88.246:8000/products/add", json=product)

if __name__ == "__main__":
    load_products_to_db()