from modules import scrape, analysis, visualizate

NUM_PAGES: int = int(input("Number of pages = ") or "100")  # Defaults to 100
SITE: str = input("News pages url = ") or "https://www.bbc.com/news"

print("Scraping the pages...")
scrape(NUM_PAGES, SITE)

analysis()

visualizate()
