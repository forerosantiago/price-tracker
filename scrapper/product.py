"""Definition of the Product class"""


class Product:
    """Definition of a product with name, url and price"""
    #Constructor method for the Product class.
    def __init__(self, name, url, price):
        self.name = name 
        self.url = url 
        self.price = price 

    def __str__(self):
        #Returned a formatted string that includes the product's name, price and URL.
        return f"{self.name} - {self.price} - {self.url}"
