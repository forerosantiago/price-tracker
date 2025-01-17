"""Definition for the Scrapper class and its subclasses"""


class Scrapper:
    """Base class for a scrapper"""

    def __init__(self):
        pass

    def search(self, term):
        """Search for a term and return a list of results"""
        raise NotImplementedError("Subclass must implement this method")

    def get_price(self, url):
        """Get the price of a product given its URL"""
        raise NotImplementedError("Subclass must implement this method")
