"""Definition of the Product class"""


class Product:
    """Definition of a product with name, url and price"""

    def __init__(self, name, url, price):
        self.name = name
        self.url = url
        self.price = price

    def __str__(self):
        return f"{self.name} - {self.price} - {self.url}"
