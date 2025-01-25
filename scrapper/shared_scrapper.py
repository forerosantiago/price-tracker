"""Definition for the SharedScrapper class that inherits from Scrapper"""

import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from scrapper.scrapper import Scrapper

from scrapper.product import Product

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

            result = Product(name, url, price)

            results.append(result)

        # close driver
        # driver.quit()
        driver.close()

        return results

    def get_price(self, url):
        # using a regex identify the domain
        domain = url.split("/")[2]

        if domain != self.domain:
            raise RuntimeError("Sitio no soportado")

        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            price_tag = soup.find("meta", {"property": "product:price:amount"})

            if price_tag:
                return float(price_tag["content"])
