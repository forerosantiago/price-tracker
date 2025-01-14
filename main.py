"""Module defining an object with a method to fetch prices from various websites."""
import requests
from bs4 import BeautifulSoup


class Product:
    """Class a prodcut with methods fo fetch prices given URLs"""
    def __init__(self, name, urls):
        self.name = name
        self.urls = urls
        self.prices = {}

    def get_prices(self):
        """Fetch prices from the provided URLs and store them in the prices dictionary."""
        for url in self.urls:
            # using a regex identify the domain
            domain = url.split("/")[2]

            if (domain == "www.exito.com" or
                domain == "www.carulla.com" or
                domain == "www.tiendasjumbo.co"):
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.content, "html.parser")
                    price_tag = soup.find("meta", {"property": "product:price:amount"})

                    if price_tag:
                        self.prices[domain] = float(price_tag["content"])
                # agregar makro
            else:
                print(f"Site {domain} not supported yet")


vino = Product(
    "Vino",
    [
        "https://www.exito.com/vino-espumoso-rose-ice-edition-x-750-ml-589856/p",
        "https://www.carulla.com/vino-espumoso-rose-ice-edition-x-750-ml-589856/p",
        "https://www.tiendasjumbo.co/vino-j-p-chenet-espumoso-ice-edition-rosado-bot-x-750ml/p"
    ],
)

vino.get_prices()
print(vino.prices)
