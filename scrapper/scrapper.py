"""Definition for the Scrapper class"""

from abc import ABC, abstractmethod

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

        profile = FirefoxProfile()
        profile.set_preference("permissions.default.image", 2)  # disable images
        profile.set_preference("permissions.default.font", 2)  # disable fonts

        options = webdriver.FirefoxOptions()
        options.profile = profile

        options.add_argument("--headless")
        # options.add_argument("--user-data-dir=cache")
        cls.driver = webdriver.Firefox(options=options)

        # path = os.path.dirname(os.path.abspath(__file__))

        # cls.driver.install_addon(
        #   os.path.join(path, "uBlock0_1.62.1b1.firefox.signed.xpi")
        # )
        return cls.driver

    @abstractmethod
    def search(self, term):
        """Search for a term and return a list of results"""
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def get_price(self, url):
        """Get the price of a product given its URL"""
        raise NotImplementedError("Subclass must implement this method")
