"""Definition for CarullaScrapper class."""
#Import SharedScrapper class from the shared_scrapper module within the scrapper package.
from scrapper.shared_scrapper import SharedScrapper

#Define the CarullaScrapper class that inherits from the SharedScrapper class.
class CarullaScrapper(SharedScrapper):
    """Class to fetch prices from www.carulla.com"""
    #Constructor method for the CarullaScrapper class.
    def __init__(self):
        #Call the constructor of the base class and pass the URL of the website to be scraped.
        super().__init__("www.carulla.com")
