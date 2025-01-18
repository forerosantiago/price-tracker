"""Definition for CarullaScrapper class."""

from scrapper import SharedScrapper


class CarullaScrapper(SharedScrapper):
    """Class to fetch prices from www.carulla.com"""

    def __init__(self):
        super().__init__("www.carulla.com")
