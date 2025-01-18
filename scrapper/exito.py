"""Definition for ExitoScrapper class."""

from scrapper import SharedScrapper


class ExitoScrapper(SharedScrapper):
    """Class to fetch prices from www.exito.com"""

    def __init__(self):
        super().__init__("www.exito.com")
