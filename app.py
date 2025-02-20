"""Main module of the application."""

import sqlite3

from flask import Flask, render_template, request
from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper

from utilities import get_product_by_id
from utilities import get_price_history_by_id
from utilities import get_product_stores_by_id

from utilities import ListedProduct

app = Flask(__name__)

# Initialize scrapers
scrapers = {
    "Exito": ExitoScrapper(),
    "Carulla": CarullaScrapper(),
    "Jumbo": JumboScrapper(),
}


@app.route("/")
def products():
    """List all products found in the database."""
    product_list = []
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        entries = cursor.execute("SELECT * FROM Products").fetchall()

        for entry in entries:
            product_id = entry[0]
            name = entry[1]
            img_url = entry[2]

            product_list.append(
                ListedProduct(
                    name,
                    url=None,
                    price=None,
                    image_url=img_url,
                    id=product_id,
                    store_name=None,
                )
            )
    return render_template("products.html", products=product_list)


# Product page with information
@app.route("/product/<int:prod_id>")
def product(prod_id):
    """Show product image, price over time graph and links."""

    return render_template(
        "product.html",
        product=get_product_by_id(prod_id),
        listed_products=get_product_stores_by_id(prod_id),
        price_history=get_price_history_by_id(prod_id),
    )


# Create a product
@app.route("/create-product", methods=["GET", "POST"])
def create_product():
    """Create a product."""
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        stores = cursor.execute("SELECT * FROM Stores").fetchall()

        # Create a row in Products table
        if request.method == "POST":
            name = request.form.get("name")
            image_url = request.form.get("image_url")

            cursor.execute(
                "INSERT OR IGNORE INTO Products (name, image_url) VALUES (?, ?)",
                (name, image_url),
            )
            row = cursor.execute(
                "SELECT id FROM Products WHERE name = ? AND image_url = ?",
                (name, image_url),
            ).fetchone()
            product_id = row[0] if row else None

            for store in stores:
                store_name = store[1]
                url = request.form[store_name]

                if url:
                    scraper = scrapers.get(store_name)

                    if scraper:
                        last_price = scraper.get_price(url)
                    else:
                        last_price = 0

                    if last_price:
                        cursor.execute(
                            """INSERT OR IGNORE INTO ProductStores
                            (product_id, store_id, name, url, last_price)
                            VALUES (?, ?, ?, ?, ?)""",
                            (product_id, store[0], store_name, url, last_price),
                        )
            conn.commit()
            return render_template(
                "create-product.html", message="Product created successfully"
            )

    return render_template("create-product.html", stores=stores)


@app.route("/update", methods=["GET", "POST"])
def updateprices():
    """Update all prices on the database."""

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        all_ids = cursor.execute("SELECT id FROM Products").fetchall()

        for product_id in all_ids:
            product_stores = cursor.execute(
                "SELECT * FROM ProductStores WHERE product_id = ?", (product_id[0],)
            ).fetchall()

            for product_store in product_stores:
                scraper = scrapers.get(product_store[3])
                if scraper:
                    price = scraper.get_price(product_store[4])

                if (
                    price == 0
                ):  # if product is not available dont register it in the database
                    continue

                cursor.execute(
                    "INSERT INTO PriceHistory (product_store_id, price) VALUES (?, ?)",
                    (product_store[0], price),
                )

        conn.commit()
    return "Prices updated successfully"


# def fetch_products(scraper, search_term):
#    """Fetch products from a given scraper."""
#    return scraper.search(search_term)

# @app.route("/search", methods=["GET", "POST"])
# def index():
# """Search page. Shows search results."""
# products = {}
# if request.method == "POST":
#     term = request.form["search_term"]
#     with ThreadPoolExecutor() as executor:
#         futures = {
#             name: executor.submit(fetch_products, scraper, term)
#             for name, scraper in scrapers.items()
#         }
#         results = {name: future.result() for name, future in futures.items()}
#         products = results
# return render_template("search.html", products=products, term=term)

if __name__ == "__main__":
    app.run(debug=True)
