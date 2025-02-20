"""This module contains utility functions for the web application and database management."""

import sqlite3
import json

from scrapper.product import Product

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper

scrapers = {
    "Exito": ExitoScrapper(),
    "Carulla": CarullaScrapper(),
    "Jumbo": JumboScrapper(),
}


class ListedProduct(Product):
    """ListedProduct extends Product to add the id attribute"""

    def __init__(self, name, url, price, image_url, id, store_name):
        super().__init__(name, url, price, image_url)
        self.store_name = store_name
        self.id = id


class Store:
    """Store class to represent a store in the database"""
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url



def list_stores():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    entries = cursor.execute("SELECT * FROM Stores").fetchall()

    stores = []
    for entry in entries:
        stores.append(Store(entry[0], entry[1], entry[2]))

    conn.close()
    return stores


def get_store_by_id(store_id):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    entries = cursor.execute("SELECT * FROM Stores WHERE id = ?", (store_id,)).fetchone()

    conn.close()
    return Store(id=entries[0], name=entries[1], url=entries[2])


def get_product_by_id(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        entry = cursor.execute("SELECT * FROM Products WHERE id = ?", (id,)).fetchone()
        
        return Product(name=entry[1], url=None, price=None, image_url=entry[2])

def get_product_stores_by_id(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        entries = cursor.execute("SELECT * FROM ProductStores WHERE product_id = ?", (id,)).fetchall()

        product_stores = []
        for entry in entries:
            product_stores.append(
                ListedProduct(
                    name=entry[3],
                    url=entry[4],
                    price=entry[5],
                    image_url=None,
                    id=entry[0],
                    store_name=get_store_by_id(entry[2]).name,
                )
            )
        return product_stores



def update_prices(product_id):

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    product_stores = cursor.execute(
        "SELECT * FROM ProductStore WHERE product_id = ?", (product_id,)
    ).fetchall()

    for product_store in product_stores:
        price = scrapers.get(product_store[3]).get_price(product_store[4])

        if price == 0: # if product is not available dont register it in the database
            continue

        cursor.execute(
            "INSERT INTO PriceHistory (product_store_id, price) VALUES (?, ?)",
            (product_store[0], price),
        )

    conn.commit()
    conn.close()




def get_price_history_by_id(product_id):
    conn = sqlite3.connect("test.db")
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

    conn.close()
    return json.dumps(price_history)
