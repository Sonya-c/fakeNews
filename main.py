from modules import scrape, analysis, visualizate, generate

NUM_PAGES: int = int(input("Number of pages = ") or "100")  # Defaults to 100

print("Scraping el sitio web...")
scrape(NUM_PAGES)

print("\nAnalizando las páginas...")
analysis("exp_1", True)

print("\nGenerando los titulares...")
generate()
analysis("exp_2")

print("\nPreparando la visualización...")
visualizate()
