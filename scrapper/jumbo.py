"""Definition for JumboScrapper class."""

import re
import requests

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from scrapper.scrapper import Scrapper

from scrapper.product import Product


class JumboScrapper(Scrapper):
    """Class to fetch prices from www.jumbo.com"""

    def __init__(self):
        super().__init__("www.jumbocolombia.com")

    def search(self, term):
        """Get the price of a product from Jumbo."""
        driver = self.get_driver()

        query = term.replace(" ", "%20")
        url = f"https://www.jumbocolombia.co/{query}?_q={query}&map=ft"
        driver.get(url)

        products = driver.find_elements(
            By.CSS_SELECTOR,
            ".tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem",
        )

        results = []
        for product in products:
            name = product.find_element(
                By.CSS_SELECTOR,
                ".vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body",
            )

            price = product.find_element(
                By.CSS_SELECTOR, ".tiendasjumboqaio-jumbo-minicart-2-x-price"
            )

            price = float(price.text.replace("$", "").replace(" ", "").replace(".", ""))

            url = product.find_element(By.TAG_NAME, "a")

            try:
                img_url = product.find_element(By.TAG_NAME, "img").get_attribute("src")
            except NoSuchElementException:
                img_url = None

            result = Product(name.text, url.get_attribute("href"), price, img_url)

            results.append(result)

        driver.close()
        return results

    def get_price(self, url):

        domain = url.split("/")[2]

        if domain != self.domain:
            raise RuntimeError("Sitio no soportado")

        r = requests.get(url, timeout=10)
        if r.status_code == 200:

            # Regular expression to extract the number after "Price":
            match = re.search(r'"Price":(\d+)', r.text)

            if match:
                price = float(match.group(1))
                return price
        return None
