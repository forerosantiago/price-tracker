"""Definition of the Product class"""


class Product:
    """Definition of a product with name, url and price"""
    #Constructor method for the Product class.
    def __init__(self, name, url, price):
        #Initialize the product's name, URL, and price attributes. 
        self.name = name #The name of the product.
        self.url = url #The URL where the product can be found.
        self.price = price #The price of the product.
    #String representation method for the Product class.
    def __str__(self):
        #Returned a formatted string that includes the product's name, price and URL.
        return f"{self.name} - {self.price} - {self.url}"
