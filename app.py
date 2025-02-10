"""Main module of the application."""

import time
import sqlite3
import schedule

from flask import Flask, render_template, request

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper
from scrapper.product import Product


from utilities import get_all_products
from utilities import update_prices
from utilities import get_product_store_s
from utilities import get_price_history_by_id


app = Flask(__name__)

# Initialize scrapers
scrapers = {
    "Exito": ExitoScrapper(),
    "Carulla": CarullaScrapper(),
    "Jumbo": JumboScrapper(),
}


def fetch_products(scraper, search_term):
    """Fetch products from a given scraper."""
    return scraper.search(search_term)


@app.route("/")
def home():
    """Home page. Currently shows a search bar."""
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def index():
    """Search page. Shows search results."""
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

    return "El dueño me desactivó <a href='/products'>Volver</a>"


@app.route("/products")
def productslist():
    """List all products found in the database."""
    return render_template("products.html", products=get_all_products())


# create route to show product information with id from database


@app.route("/product/<int:product_id>")
def product(product_id):
    """Show product image, price over time graph and links."""
    entry = (
        sqlite3.connect("test.db")
        .cursor()
        .execute("SELECT * FROM Products WHERE id = ?", (product_id,))
        .fetchone()
    )

    return render_template(
        "product.html",
        product=Product(name=entry[1], url=None, price=None, image_url=entry[2]),
        listed_products=get_product_store_s(product_id),
        price_history=get_price_history_by_id(product_id),
    )


# create create product route
@app.route("/create-product", methods=["GET", "POST"])
def create_product():
    """Create a product."""
    stores = (
        sqlite3.connect("test.db").cursor().execute("SELECT * FROM Stores").fetchall()
    )

    if request.method == "POST":
        name = request.form["name"]
        image_url = request.form["image_url"]

        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        cursor.execute(
            """INSERT OR IGNORE INTO Products (name, image_url) VALUES (?, ?)""",
            (
                name,
                image_url,
            ),
        )

        cursor.execute(
            "SELECT id FROM Products WHERE name = ? AND image_url = ?",
            (name, image_url),
        )
        row = cursor.fetchone()

        product_id = row[0] if row else None

        conn.commit()
        conn.close()

        for store in stores:
            store_name = store[1]
            store_url = request.form[store_name]
            if store_url:

                scraper = scrapers.get(store_name)

                if scraper:
                    last_price = scraper.get_price(store_url)
                else:
                    last_price = 0

                conn = sqlite3.connect("test.db")
                cursor = conn.cursor()

                cursor.execute(
                    """INSERT OR IGNORE INTO ProductStore
                        (product_id, store_id, name, url, last_price)
                        VALUES (?, ?, ?, ?, ?)""",
                    (product_id, store[0], store_name, store_url, last_price),
                )

                conn.commit()
                conn.close()

        return render_template(
            "create-product.html", message="Product created successfully"
        )

    return render_template("create-product.html", stores=stores)


def job():
    """Update prices every hour."""
    products = get_all_products()

    for item in products:
        update_prices(item.id)


@app.route("/update", methods=["GET", "POST"])
def updateprices():
    """Update all prices on the database."""
    job()
    return "Prices updated successfully"


if __name__ == "__main__":
    app.run(debug=True)

    schedule.every(5).minutes.do(job)

    time.sleep(1)
