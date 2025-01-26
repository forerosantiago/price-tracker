"""Demonstration for the scrapper module."""

from pick import pick

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper
from concurrent.futures import ThreadPoolExecutor

# Initialize scrapers
exito = ExitoScrapper()
carulla = CarullaScrapper()
jumbo = JumboScrapper()


def fetch_products(scraper, search_term):
    """Fetch products from a given scraper."""
    return scraper.search(search_term)


# Input from the user
term = input("Enter your search term: ")

# Create a ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    # Submit scraper tasks
    future_exito = executor.submit(fetch_products, exito, term)
    future_carulla = executor.submit(fetch_products, carulla, term)
    future_jumbo = executor.submit(fetch_products, jumbo, term)

    # Collect results as they finish
    exito_products = future_exito.result()
    carulla_products = future_carulla.result()
    jumbo_products = future_jumbo.result()

if exito_products:
    option_exito, index_exito = pick(exito_products, "Select a product from Exito: ")
    print(f"Selected product from Exito: {option_exito}")
else:
    print("No products found in Exito")

if carulla_products:
    option_carulla, index_carulla = pick(
        carulla_products, "Select a product from Carulla: "
    )
    print(f"Selected product from Carulla: {option_carulla}")
else:
    print("No products found in Carulla")

if jumbo_products:
    option_jumbo, index_jumbo = pick(jumbo_products, "Select a product from Jumbo: ")
    print(f"Selected product from Jumbo: {option_jumbo}")
else:
    print("No products found in Jumbo")
