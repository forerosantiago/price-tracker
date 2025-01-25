"""Definition for JumboScrapper class."""
#Import necessary libraries for regular expressions and HTTP requests.
import re
import requests
#Import the By class from Selenium to locate elements on a web page.
from selenium.webdriver.common.by import By
#Import the base Scrapper class from the scrapper module.
from scrapper.scrapper import Scrapper
#Impor the Product Class from the product module to create product objects.
from scrapper.product import Product


class JumboScrapper(Scrapper):
    """Class to fetch prices from www.jumbo.com"""
    #Constructor method for thw JumboScrapper class.
    def __init__(self):
        #Call the constructor of the base class and pass the URL of the Jumbo website.
        super().__init__("www.tiendasjumbo.co")

    def search(self, term):
        """Get the price of a product from Jumbo."""
        #Get the web driver instance for Selenium.
        driver = self.get_driver()
        #Construct the search URL using the provided search term.
        url = f"https://www.tiendasjumbo.co/{term.replace(' ', '%20')}?_q={term.replace(' ', '%20')}&map=ft"
        driver.get(url)
        #Find all product elements on the page using a CSS selector.
        products = driver.find_elements(
            By.CSS_SELECTOR,
            ".tiendasjumboqaio-cmedia-integration-cencosud-0-x-galleryItem",
        )

        results = [] #Initialize and empty list to store product results.
        for product in products:
            #Extract the product name using a CSS selector.
            name = product.find_element(
                By.CSS_SELECTOR,
                ".vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body",
            )
            #Extract the product price using a CSS selector.
            price = product.find_element(
                By.CSS_SELECTOR, ".tiendasjumboqaio-jumbo-minicart-2-x-price"
            )
            #Convert the price text to a float after cleaning it.
            price = float(price.text.replace("$", "").replace(" ", "").replace(".", ""))
            #Extract the product URL from the anchor tag.
            url = product.find_element(By.TAG_NAME, "a")
            #Create a Product object with the extracted details.
            result = Product(name.text, url.get_attribute("href"), price)
            #Append the Product object of the result list.
            results.append(result)
        #Close the web driver aftes scrapping.
        driver.close()
        return results

    def get_price(self, url):
        #Extract the domain from the provided URL.
        domain = url.split("/")[2]
        #Check if the domain matches the expected domain for Jumbo.
        if domain != self.domain:
            raise RuntimeError("Sitio no soportado")
        #Send a GET request to the provided URL with a timeout.
        r = requests.get(url, timeout=10)
        #Check if the request was successful (status code 200).
        if r.status_code == 200:

            # Regular expression to extract the number after "Price":
            match = re.search(r'"Price":(\d+)', r.text)
            #If a math is found, extract and resturn the price as a float.
            if match:
                price = float(match.group(1))
                return price
            else:
                return None #    Return None if the price is not found.
