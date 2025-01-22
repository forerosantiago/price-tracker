from pick import pick

from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper


exito = ExitoScrapper()
carulla = CarullaScrapper()
jumbo = JumboScrapper()

search_term = input("Enter your search term: ")


# Select products from each scraper
title = "Please choose a product: "

options_exito = exito.search(search_term)

option_exito, index_exito = pick(options_exito, title)
print(
    f"Selected product from Exito: {option_exito} - ${options_exito[index_exito].price}"
)


options_carulla = carulla.search(search_term)

option_carulla, index_carulla = pick(options_carulla, title)

print(
    f"Selected product from Carulla: {option_carulla} - ${options_carulla[index_carulla].price}"
)


options_jumbo = jumbo.search(search_term)

option_jumbo, index_jumbo = pick(options_jumbo, title)
print(
    f"Selected product from Jumbo: {option_jumbo} - ${options_jumbo[index_jumbo].price}"
)
