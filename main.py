"""Demonstration for the scrapper module."""

from concurrent.futures import ThreadPoolExecutor
from pick import pick
from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper

# Initialize scrapers
scrapers = {
    "Exito": ExitoScrapper(),
    "Carulla": CarullaScrapper(),
    "Jumbo": JumboScrapper()
}

def fetch_products(scraper, search_term):
    """Fetch products from a given scraper."""
    return scraper.search(search_term)

# Input from the user
term = input("Enter your search term: ")

# Create a ThreadPoolExecutor and fetch products
with ThreadPoolExecutor() as executor:
    futures = {name: executor.submit(fetch_products, scraper, term) for name, scraper in scrapers.items()}
    results = {name: future.result() for name, future in futures.items()}

# Process results
for store, products in results.items():
    if products:
        option, _ = pick(products, f"Select a product from {store}: ")
        print(f"Selected product from {store}: {option}")
    else:
        print(f"No products found in {store}")
