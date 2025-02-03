from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template, request
import sqlite3

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper

import database

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
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def index():
    products = {}
    if request.method == "POST":
        term = request.form["search_term"]
        with ThreadPoolExecutor() as executor:
            futures = {
                name: executor.submit(fetch_products, scraper, term)
                for name, scraper in scrapers.items()
            }
            results = {name: future.result() for name, future in futures.items()}
            products = results
    return render_template("search.html", products=products, term=term)


@app.route("/products")
def products():
    # connect to database and list all entries in Products table using sqlite
    products = sqlite3.connect('test.db').cursor().execute('SELECT * FROM Products').fetchall()
    
    print(products)

    return render_template("products.html", products=products)  


if __name__ == "__main__":
    app.run(debug=True)
