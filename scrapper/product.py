"""Definition of the Product class"""


class Product:
    """Definition of a product with name, url and price"""

    def __init__(self, name, url, price, image_url):
        self.name = name
        self.url = url
        self.price = price
        self.image_url = image_url

    def __str__(self):
        return f"{self.name} - {self.price} - {self.url} - {self.image_url}"
