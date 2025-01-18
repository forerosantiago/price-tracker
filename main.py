from concurrent.futures import ThreadPoolExecutor
from pick import pick


from scrapper.exito import ExitoScrapper
from scrapper.carulla import CarullaScrapper
from scrapper.jumbo import JumboScrapper


# Assuming the scrapers are already defined
exito = ExitoScrapper()
carulla = CarullaScrapper()
jumbo = JumboScrapper()


def search_exito(term):
    return exito.search(term)


def search_carulla(term):
    return carulla.search(term)


def search_jumbo(term):
    return jumbo.search(term)


# Get the search term
search_term = input("Enter your search term: ")

# Use ThreadPoolExecutor to run the searches concurrently
with ThreadPoolExecutor() as executor:
    # Submit all search tasks
    future_exito = executor.submit(search_exito, search_term)
    future_carulla = executor.submit(search_carulla, search_term)
    future_jumbo = executor.submit(search_jumbo, search_term)

    # Wait for all tasks to complete and get results
    resultados_exito = future_exito.result()
    resultados_carulla = future_carulla.result()
    resultados_jumbo = future_jumbo.result()


# use pick to select a product from each store

title = "Please choose a product: "
options_exito = [result["name"] for result in resultados_exito]
options_carulla = [result["name"] for result in resultados_carulla]
options_jumbo = [result["name"] for result in resultados_jumbo]

if options_exito != []:
    option_exito, index_exito = pick(options_exito, title)

    print(
        f"Selected product from Exito: {option_exito} - ${resultados_exito[index_exito]['price']}"
    )
if options_carulla != []:
    option_carulla, index_carulla = pick(options_carulla, title)
    print(
        f"Selected product from Carulla: {option_carulla} - ${resultados_carulla[index_carulla]['price']}"
    )

if options_jumbo != []:
    option_jumbo, index_jumbo = pick(options_jumbo, title)

    print(
        f"Selected product from Jumbo: {option_jumbo} - ${resultados_jumbo[index_jumbo]['price']}"
    )


