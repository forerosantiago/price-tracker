"""Demonstration for the scrapper module."""

from concurrent.futures import ThreadPoolExecutor
from pick import pick

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper

from database import execute_query

# Initialize scrapers
scrapers = {
    "Exito": ExitoScrapper(),
    "Carulla": CarullaScrapper(),
    "Jumbo": JumboScrapper(),
}

# Create Store entries in the database from srappers with an sql query
for name, scrapper in scrapers.items():
    execute_query(
        """
    INSERT OR IGNORE INTO Stores (name, url)
    VALUES (?, ?)
    """,
        (name, scrapper.domain),
    )


def fetch_products(scraper, search_term):
    """Fetch products from a given scraper."""
    return scraper.search(search_term)


# Input from the user
term = input("Enter your search term: ")

# Create a product entry in the database from the search term
execute_query(
    """
INSERT INTO Products (name)
VALUES (?)
""",
    (term,),
)


# Create a ThreadPoolExecutor and fetch products
with ThreadPoolExecutor() as executor:
    futures = {
        name: executor.submit(fetch_products, scraper, term)
        for name, scraper in scrapers.items()
    }
    results = {name: future.result() for name, future in futures.items()}

# Process results
for store, products in results.items():
    if products:
        option, _ = pick(products, f"Select a product from {store}: ")
        print(f"Selected product from {store}: {option}")

        # Create a ProductStore entry
        execute_query(
            """
        INSERT INTO ProductStore (product_id, store_id, name, url, last_price)
        VALUES (
            (SELECT id FROM Products WHERE name = ?),
            (SELECT id FROM Stores WHERE name = ?),
            ?, ?, ?
        )
        """,
            (term, store, option.name, option.url, option.price),
        )
    else:
        print(f"No products found in {store}")
