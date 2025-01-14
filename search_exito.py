"""Module providing a function that searches products on Exito.com."""

from selenium import webdriver
from selenium.webdriver.common.by import By


def search_exito(term):
    """Search a product on Exito and print the result's full name, price and URL."""
    driver = webdriver.Firefox()

    url = f"https://www.exito.com/s?q={term.replace(' ', '-')}&sort=score_desc&page=0"

    driver.get(url)

    # find ul element by xpath
    xpath = "/html/body/div[1]/main/section[3]/div/div[2]/div[2]/div[2]/ul"
    ul_element = driver.find_element(By.XPATH, xpath)

    # find all li elements within the ul element
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    results = []

    for index, li in enumerate(li_elements, start=1):
        product_info = li.text.split("\n")
        name = product_info[0]
        for line in product_info:
            if line.startswith("$"):
                price = line
                # remove $ spaces and . in price
                price = price.replace("$", "")
                price = price.replace(" ", "")
                price = price.replace(".", "")
                price = float(price)
                break

        a_element = li.find_element(By.TAG_NAME, "a")
        url = a_element.get_attribute("href")

        result = {
            "name": name,
            "price": price,
            "url": url
        }

        results.append(result)

    return results

    
