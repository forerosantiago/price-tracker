"""Definition for the Scrapper class and its subclasses"""

from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class Scrapper(ABC):
    """Base class for a scrapper"""

    def __init__(self, domain):
        self.domain = domain

    driver = None  # WebDriver instance shared among all scrappers

    @classmethod
    def get_driver(cls):
        """Return the shared WebDriver instance."""
        if cls.driver is None:
            profile = FirefoxProfile()
            profile.set_preference("permissions.default.image", 2)

            options = webdriver.FirefoxOptions()
            options.profile = profile

            # options.add_argument("--headless")
            options.add_argument("--user-data-dir=cache")
            cls.driver = webdriver.Firefox(options=options)
        return cls.driver

    @abstractmethod
    def search(self, term):
        """Search for a term and return a list of results"""
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def get_price(self, url):
        """Get the price of a product given its URL"""
        raise NotImplementedError("Subclass must implement this method")


class SharedScrapper(Scrapper):
    """Subclass for www.exito.com, www.carulla.com and www.tiendasjumbo.co"""

    @abstractmethod
    def search(self, term):
        pass

    def get_price(self, url):
        # using a regex identify the domain
        domain = url.split("/")[2]

        if self.domain != domain:
            raise ValueError(f"Site {domain} is not supported by this class!")

        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            price_tag = soup.find("meta", {"property": "product:price:amount"})

            if price_tag:
                return float(price_tag["content"])
