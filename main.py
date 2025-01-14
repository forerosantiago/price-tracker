"""Module defining an object with a method to fetch prices from various websites."""
import requests
from bs4 import BeautifulSoup
from prettytable.colortable import ColorTable, Themes
from search_exito import search_exito

class Product:
    """Class of a product with methods fo fetch prices given URLs"""

    def __init__(self, name, urls=None):
        self.name = name

        if urls is None:
            self.urls = []
        self.prices = {}

    def set_exito_url(self, term):
        """Search for a product on Exito and add the URL to the list of URLs."""
        results = search_exito(term)

        if not results:
            print("No results found")
            return
        else:
            print(f"Found {len(results)} results for {term}")
            table = ColorTable(theme=Themes.OCEAN)
            table.field_names = ["#", "Name", "Price"]

            for index, result in enumerate(results):
                table.add_row([index, result["name"], result["price"]])
                # print(f"URL: {result['url']}")

            print(table)

            input_index = input(
                "Enter the index of the product you want to add to the list: "
            )
            print(results[int(input_index)]["url"])

            self.urls.append(results[int(input_index)]["url"])

    def get_prices(self):
        """Fetch prices from the provided URLs and store them in the prices dictionary."""
        for url in self.urls:
            # using a regex identify the domain
            domain = url.split("/")[2]

            if (
                domain == "www.exito.com"
                or domain == "www.carulla.com"
                or domain == "www.tiendasjumbo.co"
            ):
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.content, "html.parser")
                    price_tag = soup.find("meta", {"property": "product:price:amount"})

                    if price_tag:
                        self.prices[domain] = float(price_tag["content"])
                # agregar makro
            else:
                print(f"Site {domain} not supported yet")


search_term = input("Enter the product you want to search: ")
test_product = Product(search_term)
test_product.set_exito_url(search_term)

test_product.get_prices()

print(test_product.prices)
print(test_product.urls)
