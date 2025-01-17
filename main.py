"""Module defining an object with a method to fetch prices from various websites."""

from prettytable.colortable import ColorTable, Themes
from scrapper.exito import ExitoScrapper


class Product:
    """Class of a product with methods fo fetch prices given URLs"""

    def __init__(self, name, urls=None):
        self.name = name

        if urls is None:
            self.urls = []
        self.prices = {}

    def set_exito_url(self, term):
        """Search for a product on Exito and add the URL to the list of URLs."""
        scrappeador = ExitoScrapper()

        results = scrappeador.search(term)

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


test_product = Product("Arroz")
test_product.set_exito_url("arroz")
