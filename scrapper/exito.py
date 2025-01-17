"""Definition for ExitoScrapper class."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from scrapper import SharedScrapper


class ExitoScrapper(SharedScrapper):
    """Scrapper class for Exito.com website"""

    def __init__(self):
        super().__init__("www.exito.com")

    def search(self, term):
        # or domain == "www.tiendasjumbo.co"
        profile = FirefoxProfile()
        profile.set_preference("permissions.default.image", 2)

        options = webdriver.FirefoxOptions()
        options.profile = profile

        # options.add_argument("--headless")
        options.add_argument("--user-data-dir=cache")
        driver = webdriver.Firefox(options=options)

        url = (
            f"https://www.exito.com/s?q={term.replace(' ', '-')}&sort=score_desc&page=0"
        )

        driver.get(url)

        # find ul element by xpath
        xpath = "/html/body/div[1]/main/section[3]/div/div[2]/div[2]/div[2]/ul"

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
