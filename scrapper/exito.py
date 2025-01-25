"""Definition for ExitoScrapper class."""
#Import the SharedScrapper class from the share_scrapper module within the scrapper package.
from scrapper.shared_scrapper import SharedScrapper

#Define the ExitoScrapper class that inherits from the SharedScrapper class.
class ExitoScrapper(SharedScrapper):
    """Class to fetch prices from www.exito.com"""
    #Constructor methos for the ExitoScrapper class.
    def __init__(self):
        #Call the constructor of the base class (SharedScrapper) and pass the URL of the website to be scrapped.
        super().__init__("www.exito.com")
