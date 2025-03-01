"""This module contains utility functions for the web application and database management."""

import sqlite3
import json

from scrapper.product import Product

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper

# Dictionary mapping store names to their respective scraper instances
scrapers = {
    "Exito": ExitoScrapper(),
    "Carulla": CarullaScrapper(),
    "Jumbo": JumboScrapper(),
}

# ListedProduct extends the Product class to include additional attributes like id and store_name
class ListedProduct(Product):
    """ListedProduct extends Product to add the id attribute"""

    def __init__(self, name, url, price, image_url, id, store_name):
        super().__init__(name, url, price, image_url)
        self.store_name = store_name
        self.id = id

# Store class to represent a store in the database
class Store:
    """Store class to represent a store in the database"""

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url

# Retrieve a product from the database by its ID.
def get_product_by_id(id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        entry = cursor.execute("SELECT * FROM Products WHERE id = ?", (id,)).fetchone()

        return Product(name=entry[1], url=None, price=None, image_url=entry[2])

# Retrieve all stores that list a product by the product's ID.
def get_product_stores_by_id(id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        entries = cursor.execute(
            "SELECT * FROM ProductStores WHERE product_id = ?", (id,)
        ).fetchall()

        product_stores = []
        for entry in entries:
            store_name = cursor.execute("SELECT name FROM Stores WHERE id = ?", (entry[2],)).fetchone()[0]
            product_stores.append(
                ListedProduct(
                    name=entry[3],
                    url=entry[4],
                    price=entry[5],
                    image_url=None,
                    id=entry[0],
                    store_name=store_name,
                )
            )
        return product_stores

# Retrieve the price history of a product by its ID.
def get_price_history_by_id(product_id):
    """Returns a json object with the price history of a given product id"""
    with sqlite3.connect("database.db") as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()

        price_history = {}

        productstores = get_product_stores_by_id(product_id)

        for product_store in productstores:
            price_history[product_store.name] = {}

            results = cursor.execute(
                "SELECT * FROM PriceHistory WHERE product_store_id = ?", (product_store.id,)
            ).fetchall()

            price_history[product_store.name]["time"] = []
            price_history[product_store.name]["price"] = []

            for result in results:
                price_history[product_store.name]["time"].append(result[3])

                price_history[product_store.name]["price"].append(result[2])

    return json.dumps(price_history)
