"""Definition for the Scrapper class and its subclasses"""

from abc import ABC, abstractmethod

import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


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


class SharedScrapper(Scrapper):
    """Subclass for www.exito.com, www.carulla.com and www.tiendasjumbo.co"""

    def search(self, term):
        # or domain == "www.tiendasjumbo.co"

        if self.domain == "www.exito.com":
            url = f"https://www.exito.com/s?q={term.replace(' ', '-')}&sort=score_desc&page=0"
        elif self.domain == "www.carulla.com":
            url = f"https://www.carulla.com/s?q={term.replace(' ', '+')}&sort=score_desc&page=0"
        else:
            print("Error")
            return []

        driver = self.get_driver()

        if self.domain == "www.exito.com" or self.domain == "www.carulla.com":
            xpath = "/html/body/div[1]/main/section[3]/div/div[2]/div[2]/div[2]/ul"
        else:
            xpath = ""  # otra cosa

        driver.get(url)

        try:
            ul_element = driver.find_element(By.XPATH, xpath)

        except NoSuchElementException:
            driver.quit()
            return []
        # find all li elements within the ul element

        li_elements = ul_element.find_elements(By.TAG_NAME, "li")

        results = []
        for li in li_elements:
            try:
                name_element = li.find_element(By.CSS_SELECTOR, "p.styles_name__qQJiK")
                name = name_element.get_attribute("innerHTML")
            except NoSuchElementException:
                name = None
                break

            try:
                price_element = li.find_element(
                    By.CSS_SELECTOR, 'p[data-fs-container-price-otros="true"]'
                )
                price = price_element.get_attribute("innerHTML")
                # Remove $ spaces and . in price
                price = price.replace("$", "").replace(" ", "").replace(".", "")
                price = float(price)

            except NoSuchElementException:
                price = None
                break

            a_element = li.find_element(By.TAG_NAME, "a")
            url = a_element.get_attribute("href")

            result = {"name": name, "price": price, "url": url}

            results.append(result)

        return results

    def get_price(self, url):
        # using a regex identify the domain
        domain = url.split("/")[2]

        if domain != self.domain:
            print("Error sitio no soportado")
            raise ValueError("Sitio no soportado")

        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            price_tag = soup.find("meta", {"property": "product:price:amount"})

            if price_tag:
                return float(price_tag["content"])
