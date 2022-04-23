from modules import scrape, analysis, visualizate, generate

NUM_PAGES: int = int(input("Number of pages = ") or "100")  # Defaults to 100

print("Scraping the website...")
# scrape(NUM_PAGES)

print("\nAnalyzing the pages...")
analysis()

print("\nGenerating the titles...")
# generate()

print("\npreparing to vizualizate...")
# visualizate()
