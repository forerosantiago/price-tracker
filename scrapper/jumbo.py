"""Definition for JumboScrapper class."""

from selenium.webdriver.common.by import By

from scrapper import Scrapper

from scrapper.product import Product


class JumboScrapper(Scrapper):
    """Class to fetch prices from www.jumbo.com"""

    def __init__(self):
        super().__init__("www.tiendasjumbo.co")

    def search(self, term):
        """Get the price of a product from Jumbo."""
        driver = self.get_driver()

        url = f"https://www.tiendasjumbo.co/{term.replace(' ', '%20')}?_q={term.replace(' ', '%20')}&map=ft"
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

            result = Product(name.text, url.get_attribute("href"), price)

            results.append(result)

        driver.close()
        return results

    def get_price(self, url):
        return "sapa"